// Unit tests for js/stats.js. Run with: node --test tests/stats.test.mjs
// Reference values come from R 4.6 (pnorm, qnorm, pt, lm, quantile type 7).
import { test } from "node:test";
import assert from "node:assert/strict";
import {
  rng, mean, sd, variance, quantile, cor, fmt, pct,
  pnorm, qnorm, dnorm, pt, pValue, normalPosterior, lm, ols, ridge, twoGroup
} from "../js/stats.js";

const close = (got, want, tol, what) =>
  assert.ok(Math.abs(got - want) <= tol, `${what}: got ${got}, want ${want} (tol ${tol})`);

test("pnorm matches R to 2e-7 (Abramowitz-Stegun 7.1.26)", () => {
  const z = [-3, -1.96, -0.5, 0, 0.5, 1.96, 3];
  const r = [0.00134989803163009, 0.0249978951482204, 0.308537538725987, 0.5,
    0.691462461274013, 0.97500210485178, 0.99865010196837];
  z.forEach((v, i) => close(pnorm(v), r[i], 2e-7, `pnorm(${v})`));
});

test("qnorm matches R to 1e-8 (Acklam) and inverts pnorm", () => {
  const p = [0.001, 0.025, 0.1, 0.5, 0.9, 0.975, 0.999];
  const r = [-3.09023230616781, -1.95996398454005, -1.2815515655446, 0,
    1.2815515655446, 1.95996398454005, 3.09023230616781];
  p.forEach((v, i) => close(qnorm(v), r[i], 1e-8, `qnorm(${v})`));
  for (const v of [0.01, 0.3, 0.7, 0.99]) close(pnorm(qnorm(v)), v, 3e-7, `pnorm(qnorm(${v}))`);
});

test("dnorm matches R", () => {
  close(dnorm(0), 0.398942280401433, 1e-14, "dnorm(0)");
  close(dnorm(1), 0.241970724519143, 1e-14, "dnorm(1)");
  close(dnorm(-2), 0.0539909665131881, 1e-14, "dnorm(-2)");
  close(dnorm(3, 1, 2), dnorm(1) / 2, 1e-14, "dnorm(3, 1, 2)");
});

test("pt matches R for 3, 12 and 100 degrees of freedom", () => {
  const cases = [
    [3, [-2.5, -1, 0, 1, 2.1, 4], [0.0438533235040328, 0.195501109477885, 0.5,
      0.804498890522115, 0.936717398725158, 0.985995771994927]],
    [12, [-2, 0.5, 1.7, 2.8], [0.034327507019043, 0.686941261887338,
      0.942560067302395, 0.9919778758814]],
    [100, [1.96, 2.5], [0.973610549316885, 0.992977105437961]]
  ];
  for (const [df, t, r] of cases) t.forEach((v, i) => close(pt(v, df), r[i], 1e-9, `pt(${v}, ${df})`));
});

test("pValue: normal reference without df, t reference with df", () => {
  close(pValue(1.96, 1), 0.05, 1e-4, "pValue(1.96, 1)");
  close(pValue(2.8, 1, 12), 2 * (1 - 0.9919778758814), 1e-9, "pValue(2.8, 1, 12)");
});

test("summaries: mean, sd, variance, quantile (R type 7), cor", () => {
  const y = [3.1, 4.9, 7.2, 8.8, 11.1, 12.9, 15.2, 17.1];
  close(mean(y), 10.0375, 1e-12, "mean");
  close(sd(y), 4.9274558778919, 1e-12, "sd");
  close(variance(y), 4.9274558778919 ** 2, 1e-10, "variance");
  const q = [5, 1, 4, 2, 3, 10];
  [[0.1, 1.5], [0.25, 2.25], [0.5, 3.5], [0.9, 7.5]].forEach(([p, r]) => close(quantile(q, p), r, 1e-12, `quantile ${p}`));
  close(cor([1, 2, 3, 4, 5, 6, 7, 8], y), 0.999547056448102, 1e-12, "cor");
});

test("lm and ols match R's lm()", () => {
  const x = [1, 2, 3, 4, 5, 6, 7, 8], x2 = [2, 1, 4, 3, 6, 5, 8, 9];
  const y = [3.1, 4.9, 7.2, 8.8, 11.1, 12.9, 15.2, 17.1];
  const f = lm(x, y);
  close(f.a, 0.989285714285714, 1e-10, "lm a");
  close(f.b, 2.01071428571429, 1e-10, "lm b");
  close(f.seA, 0.124804268525467, 1e-10, "lm seA");
  close(f.seB, 0.0247149279666984, 1e-10, "lm seB");
  close(f.sigma, 0.160171039532001, 1e-10, "lm sigma");
  close(f.r2, 0.999094318054066, 1e-10, "lm r2");
  const g = ols(x.map((v, i) => [v, x2[i]]), y);
  [0.999019607843137, 1.86470588235294, 0.136274509803921].forEach((v, i) => close(g.coef[i], v, 1e-9, `ols coef ${i}`));
  [0.0475869062725943, 0.0259942619285545, 0.0226128678326878].forEach((v, i) => close(g.se[i], v, 1e-9, `ols se ${i}`));
  close(g.sigma, 0.0610367937893072, 1e-10, "ols sigma");
});

test("ridge with lambda 0 is least squares; a large lambda shrinks toward zero", () => {
  const x = [1, 2, 3, 4, 5, 6, 7, 8], x2 = [2, 1, 4, 3, 6, 5, 8, 9];
  const y = [3.1, 4.9, 7.2, 8.8, 11.1, 12.9, 15.2, 17.1];
  const X = x.map((v, i) => [v, x2[i]]);
  const r0 = ridge(X, y, 0);
  close(r0.b[0], 1.86470588235294, 1e-6, "ridge(0) b1");
  close(r0.a, 0.999019607843137, 1e-6, "ridge(0) a");
  const big = ridge(X, y, 1e6);
  assert.ok(Math.abs(big.b[0]) < 0.01 && Math.abs(big.b[1]) < 0.01, "large lambda shrinks coefficients");
  close(big.a, mean(y), 0.1, "large lambda: intercept near mean(y)");
});

test("normalPosterior is the precision-weighted average", () => {
  const p = normalPosterior(0, 1, 2, 1);
  close(p.mean, 1, 1e-12, "mean");
  close(p.sd, Math.SQRT1_2, 1e-12, "sd");
});

test("rng is reproducible for a seed and differs across seeds", () => {
  assert.deepEqual(rng(7).normals(5), rng(7).normals(5));
  assert.notDeepEqual(rng(7).normals(5), rng(8).normals(5));
  const u = rng(1);
  for (let i = 0; i < 1000; i++) { const v = u(); assert.ok(v >= 0 && v < 1); }
});

test("distribution helpers have the right means and variances", () => {
  const r = rng(2026), N = 200000;
  const draw = (f) => Array.from({ length: N }, f);
  const z = draw(() => r.normal(1, 2));
  close(mean(z), 1, 0.02, "normal mean"); close(sd(z), 2, 0.02, "normal sd");
  close(mean(draw(() => r.binomial(10, 0.3))), 3, 0.02, "binomial mean");
  close(mean(draw(() => r.poisson(4))), 4, 0.02, "poisson(4) mean");
  close(mean(draw(() => r.poisson(80))), 80, 0.1, "poisson(80) mean");
  const g = draw(() => r.gamma(2.5, 2));
  close(mean(g), 5, 0.05, "gamma mean"); close(variance(g), 10, 0.3, "gamma variance");
  close(mean(draw(() => r.gamma(0.5, 1))), 0.5, 0.01, "gamma(shape < 1) mean");
  close(mean(draw(() => r.beta(2, 5))), 2 / 7, 0.005, "beta mean");
  close(mean(draw(() => r.exponential(2))), 0.5, 0.01, "exponential mean");
  close(variance(draw(() => r.t(6))), 1.5, 0.05, "t(6) variance");
  close(mean(draw(() => r.uniform(2, 4))), 3, 0.01, "uniform mean");
  const ints = draw(() => r.int(1, 6));
  assert.ok(ints.reduce((a, b) => Math.min(a, b)) === 1 && ints.reduce((a, b) => Math.max(a, b)) === 6, "int covers its range");
});

test("twoGroup: Welch test keeps its false-positive rate near 5% for small n", () => {
  const r = rng(11);
  let hits = 0;
  for (let k = 0; k < 4000; k++) if (twoGroup(r, 8, 0, 1).p < 0.05) hits++;
  close(hits / 4000, 0.05, 0.012, "false-positive rate");
});

test("fmt never prints -0.00 and shows a dash for NaN", () => {
  assert.equal(fmt(-0.001), "0.00");
  assert.equal(fmt(-0.004, 2), "0.00");
  assert.equal(fmt(-1.234), "-1.23");
  assert.equal(fmt(NaN), "–");
  assert.equal(fmt(Infinity), "–");
  assert.equal(pct(0.1234, 1), "12.3%");
});

test("debounce passes one input event after the reader pauses", async () => {
  const { debounce } = await import("../js/stats.js");
  const el = new EventTarget();
  debounce(el, 50);
  let seen = 0;
  el.addEventListener("input", () => seen++);   // registered later, like OJS's listener
  for (let i = 0; i < 5; i++) el.dispatchEvent(new Event("input"));
  assert.equal(seen, 0, "no events pass while the slider is moving");
  await new Promise((r) => setTimeout(r, 120));
  assert.equal(seen, 1, "exactly one event passes after the pause");
});
