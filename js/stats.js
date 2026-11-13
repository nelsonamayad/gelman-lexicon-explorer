// Shared simulation helpers for every concept page.
// Import from a concept page with:
//   import {rng, mean, lm} from "../js/stats.js"
// Everything is deterministic given a seed, so a page's "Random seed" slider
// reproduces the same draws.

// ---------- Random number generation ----------

// Seeded uniform generator (mulberry32) with distribution helpers attached.
export function rng(seed = 1) {
  let a = (seed * 2654435761) >>> 0;
  const u = () => {
    a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
  let spare = null;
  u.uniform = (lo = 0, hi = 1) => lo + (hi - lo) * u();
  u.int = (lo, hi) => lo + Math.floor(u() * (hi - lo + 1));
  u.normal = (mu = 0, sd = 1) => {
    if (spare !== null) {
      const z = spare;
      spare = null;
      return mu + sd * z;
    }
    let x, y, s;
    do {
      x = 2 * u() - 1;
      y = 2 * u() - 1;
      s = x * x + y * y;
    } while (s >= 1 || s === 0);
    const m = Math.sqrt((-2 * Math.log(s)) / s);
    spare = y * m;
    return mu + sd * x * m;
  };
  u.normals = (n, mu = 0, sd = 1) => Array.from({ length: n }, () => u.normal(mu, sd));
  u.bernoulli = (p) => (u() < p ? 1 : 0);
  u.binomial = (n, p) => {
    let k = 0;
    for (let i = 0; i < n; i++) if (u() < p) k++;
    return k;
  };
  u.exponential = (rate = 1) => -Math.log(1 - u()) / rate;
  u.poisson = (lambda) => {
    if (lambda > 50) return Math.max(0, Math.round(u.normal(lambda, Math.sqrt(lambda))));
    const L = Math.exp(-lambda);
    let k = 0, p = 1;
    do {
      k++;
      p *= u();
    } while (p > L);
    return k - 1;
  };
  u.gamma = (shape, scale = 1) => {
    if (shape < 1) return u.gamma(shape + 1, scale) * Math.pow(u(), 1 / shape);
    const d = shape - 1 / 3, c = 1 / Math.sqrt(9 * d);
    for (;;) {
      let x, v;
      do {
        x = u.normal();
        v = 1 + c * x;
      } while (v <= 0);
      v = v * v * v;
      const w = u();
      if (w < 1 - 0.0331 * x ** 4 || Math.log(w) < 0.5 * x * x + d * (1 - v + Math.log(v)))
        return d * v * scale;
    }
  };
  u.beta = (a, b) => {
    const x = u.gamma(a), y = u.gamma(b);
    return x / (x + y);
  };
  u.chisq = (df) => u.gamma(df / 2, 2);
  u.t = (df) => u.normal() / Math.sqrt(u.chisq(df) / df);
  u.cauchy = () => Math.tan(Math.PI * (u() - 0.5));
  u.lognormal = (mu = 0, sd = 1) => Math.exp(u.normal(mu, sd));
  u.pick = (arr) => arr[Math.floor(u() * arr.length)];
  u.shuffle = (arr) => {
    const a2 = arr.slice();
    for (let i = a2.length - 1; i > 0; i--) {
      const j = Math.floor(u() * (i + 1));
      [a2[i], a2[j]] = [a2[j], a2[i]];
    }
    return a2;
  };
  return u;
}

// ---------- Sequences and summaries ----------

export const range = (n) => Array.from({ length: n }, (_, i) => i);
export const seq = (lo, hi, n) =>
  Array.from({ length: n }, (_, i) => lo + ((hi - lo) * i) / (n - 1));
export const sum = (x) => x.reduce((s, v) => s + v, 0);
export const mean = (x) => sum(x) / x.length;
export const variance = (x) => {
  const m = mean(x);
  return sum(x.map((v) => (v - m) ** 2)) / (x.length - 1);
};
export const sd = (x) => Math.sqrt(variance(x));
export const quantile = (x, p) => {
  const s = x.slice().sort((a, b) => a - b);
  const h = (s.length - 1) * p, lo = Math.floor(h), hi = Math.ceil(h);
  return s[lo] + (s[hi] - s[lo]) * (h - lo);
};
export const median = (x) => quantile(x, 0.5);
export const cor = (x, y) => {
  const mx = mean(x), my = mean(y);
  let sxy = 0, sxx = 0, syy = 0;
  for (let i = 0; i < x.length; i++) {
    sxy += (x[i] - mx) * (y[i] - my);
    sxx += (x[i] - mx) ** 2;
    syy += (y[i] - my) ** 2;
  }
  return sxy / Math.sqrt(sxx * syy);
};
export const clamp = (v, lo, hi) => Math.min(hi, Math.max(lo, v));
// Format a number with d decimals. Never prints "-0.00", and shows "–" when
// the value is undefined (NaN or infinite), for example a mean of no values.
export const fmt = (v, d = 2) => {
  if (!Number.isFinite(v)) return "–";
  const s = v.toFixed(d);
  return /^-0\.?0*$/.test(s) ? s.slice(1) : s;
};
export const pct = (v, d = 0) => (100 * v).toFixed(d) + "%";

// ---------- Distributions ----------

export const dnorm = (x, mu = 0, s = 1) =>
  Math.exp(-0.5 * ((x - mu) / s) ** 2) / (s * Math.sqrt(2 * Math.PI));

// Standard normal CDF (Abramowitz-Stegun 7.1.26 via erf).
export function pnorm(z) {
  const t = 1 / (1 + 0.3275911 * Math.abs(z) / Math.SQRT2);
  const y =
    1 -
    (((((1.061405429 * t - 1.453152027) * t + 1.421413741) * t - 0.284496736) * t +
      0.254829592) *
      t) *
      Math.exp(-(z * z) / 2);
  return z >= 0 ? 0.5 * (1 + y) : 0.5 * (1 - y);
}

// Standard normal quantile (Acklam's approximation).
export function qnorm(p) {
  const a = [-39.6968302866538, 220.946098424521, -275.928510446969, 138.357751867269, -30.6647980661472, 2.50662827745924];
  const b = [-54.4760987982241, 161.585836858041, -155.698979859887, 66.8013118877197, -13.2806815528857];
  const c = [-0.00778489400243029, -0.322396458041136, -2.40075827716184, -2.54973253934373, 4.37466414146497, 2.93816398269878];
  const d = [0.00778469570904146, 0.32246712907004, 2.445134137143, 3.75440866190742];
  const pl = 0.02425;
  if (p < pl) {
    const q = Math.sqrt(-2 * Math.log(p));
    return (((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) /
      ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1);
  }
  if (p > 1 - pl) return -qnorm(1 - p);
  const q = p - 0.5, r = q * q;
  return ((((((a[0] * r + a[1]) * r + a[2]) * r + a[3]) * r + a[4]) * r + a[5]) * q) /
    (((((b[0] * r + b[1]) * r + b[2]) * r + b[3]) * r + b[4]) * r + 1);
}

// Log gamma (Lanczos approximation, g = 7).
function lgamma(x) {
  const c = [0.99999999999980993, 676.5203681218851, -1259.1392167224028, 771.32342877765313,
    -176.61502916214059, 12.507343278686905, -0.13857109526572012, 9.9843695780195716e-6, 1.5056327351493116e-7];
  if (x < 0.5) return Math.log(Math.PI / Math.abs(Math.sin(Math.PI * x))) - lgamma(1 - x);
  x -= 1;
  let a = c[0];
  const t = x + 7.5;
  for (let i = 1; i < 9; i++) a += c[i] / (x + i);
  return 0.5 * Math.log(2 * Math.PI) + (x + 0.5) * Math.log(t) - t + Math.log(a);
}

// Regularized incomplete beta I_x(a, b), by continued fraction (Numerical Recipes).
function ibeta(x, a, b) {
  if (x <= 0) return 0;
  if (x >= 1) return 1;
  const front = Math.exp(lgamma(a + b) - lgamma(a) - lgamma(b) + a * Math.log(x) + b * Math.log(1 - x));
  if (x > (a + 1) / (a + b + 2)) return 1 - ibeta(1 - x, b, a);
  let f = 1, c = 1, d = 1 - (a + b) * x / (a + 1);
  d = Math.abs(d) < 1e-300 ? 1e300 : 1 / d;
  f = d;
  for (let m = 1; m <= 300; m++) {
    for (const num of [m * (b - m) * x / ((a + 2 * m - 1) * (a + 2 * m)), -(a + m) * (a + b + m) * x / ((a + 2 * m) * (a + 2 * m + 1))]) {
      d = 1 + num * d; d = Math.abs(d) < 1e-300 ? 1e300 : 1 / d;
      c = 1 + num / c; if (Math.abs(c) < 1e-300) c = 1e-300;
      f *= d * c;
    }
    if (Math.abs(d * c - 1) < 1e-12) break;
  }
  return front * f / a;
}

// Student t CDF with df degrees of freedom.
export function pt(t, df) {
  const tail = 0.5 * ibeta(df / (df + t * t), df / 2, 0.5);
  return t >= 0 ? 1 - tail : tail;
}

// Two-sided p-value for est / se: against the normal distribution, or against
// a t distribution when df is given (use it for small samples).
export const pValue = (est, se, df) =>
  df ? 2 * (1 - pt(Math.abs(est / se), df)) : 2 * (1 - pnorm(Math.abs(est / se)));
export const logit = (p) => Math.log(p / (1 - p));
export const invLogit = (x) => 1 / (1 + Math.exp(-x));

// Conjugate normal update: prior N(m0, s0) and estimate y with standard error se.
export function normalPosterior(m0, s0, y, se) {
  const w0 = 1 / s0 ** 2, w1 = 1 / se ** 2;
  return { mean: (w0 * m0 + w1 * y) / (w0 + w1), sd: Math.sqrt(1 / (w0 + w1)) };
}

// ---------- Regression ----------

// Simple linear regression y = a + b x.
export function lm(x, y) {
  const n = x.length, mx = mean(x), my = mean(y);
  let sxy = 0, sxx = 0;
  for (let i = 0; i < n; i++) {
    sxy += (x[i] - mx) * (y[i] - my);
    sxx += (x[i] - mx) ** 2;
  }
  const b = sxy / sxx, a = my - b * mx;
  const resid = y.map((v, i) => v - a - b * x[i]);
  const sigma = Math.sqrt(sum(resid.map((r) => r * r)) / (n - 2));
  const seB = sigma / Math.sqrt(sxx);
  const seA = sigma * Math.sqrt(1 / n + mx ** 2 / sxx);
  const r2 = 1 - sum(resid.map((r) => r * r)) / sum(y.map((v) => (v - my) ** 2));
  return { a, b, seA, seB, sigma, r2, predict: (v) => a + b * v };
}

// Multiple regression by least squares. X is an array of rows (no intercept
// column needed: one is added). Returns coefficients and standard errors with
// the intercept first.
export function ols(X, y) {
  const n = y.length, rows = X.map((r) => [1, ...r]), k = rows[0].length;
  const XtX = Array.from({ length: k }, () => new Array(k).fill(0));
  const Xty = new Array(k).fill(0);
  for (let i = 0; i < n; i++)
    for (let j = 0; j < k; j++) {
      Xty[j] += rows[i][j] * y[i];
      for (let l = 0; l < k; l++) XtX[j][l] += rows[i][j] * rows[i][l];
    }
  const inv = invert(XtX);
  const coef = inv.map((r) => sum(r.map((v, j) => v * Xty[j])));
  const resid = y.map((v, i) => v - sum(rows[i].map((x, j) => x * coef[j])));
  const s2 = sum(resid.map((r) => r * r)) / (n - k);
  return { coef, se: inv.map((r, j) => Math.sqrt(s2 * r[j])), sigma: Math.sqrt(s2) };
}

// Ridge regression: minimizes ||y - a - Xb||^2 + lambda ||b||^2. Columns of X
// are centred internally; the intercept is not penalized. lambda = 0 gives
// least squares (when X'X is invertible). Returns {a, b, predict}.
export function ridge(X, y, lambda) {
  const n = y.length, k = X[0].length;
  const mx = Array.from({ length: k }, (_, j) => mean(X.map((r) => r[j])));
  const my = mean(y);
  const XtX = Array.from({ length: k }, () => new Array(k).fill(0));
  const Xty = new Array(k).fill(0);
  for (let i = 0; i < n; i++) {
    const xc = X[i].map((v, j) => v - mx[j]);
    for (let j = 0; j < k; j++) {
      Xty[j] += xc[j] * (y[i] - my);
      for (let l = 0; l < k; l++) XtX[j][l] += xc[j] * xc[l];
    }
  }
  for (let j = 0; j < k; j++) XtX[j][j] += lambda + 1e-9;
  const inv = invert(XtX);
  const b = inv.map((r) => sum(r.map((v, j) => v * Xty[j])));
  const a = my - sum(b.map((bj, j) => bj * mx[j]));
  return { a, b, predict: (row) => a + sum(row.map((v, j) => v * b[j])) };
}

function invert(M) {
  const n = M.length, A = M.map((r, i) => [...r, ...M.map((_, j) => (i === j ? 1 : 0))]);
  for (let c = 0; c < n; c++) {
    let p = c;
    for (let r = c + 1; r < n; r++) if (Math.abs(A[r][c]) > Math.abs(A[p][c])) p = r;
    [A[c], A[p]] = [A[p], A[c]];
    const d = A[c][c];
    for (let j = 0; j < 2 * n; j++) A[c][j] /= d;
    for (let r = 0; r < n; r++)
      if (r !== c) {
        const f = A[r][c];
        for (let j = 0; j < 2 * n; j++) A[r][j] -= f * A[c][j];
      }
  }
  return A.map((r) => r.slice(n));
}

// ---------- Common experiment ----------

// A two-group experiment with n per arm, true effect `effect` and outcome sd
// `sigma`. Returns the difference in means, its standard error and the
// p-value of Welch's t test (t reference distribution, so small samples keep
// their nominal false-positive rate).
export function twoGroup(r, n, effect, sigma = 1) {
  const t = r.normals(n, effect, sigma), c = r.normals(n, 0, sigma);
  const est = mean(t) - mean(c);
  const vt = variance(t) / n, vc = variance(c) / n;
  const se = Math.sqrt(vt + vc);
  const df = (vt + vc) ** 2 / (vt ** 2 / (n - 1) + vc ** 2 / (n - 1));
  return { est, se, df, p: pValue(est, se, df), z: est / se };
}

// ---------- Inputs ----------

// Wrap a control so the simulation recomputes only when the reader pauses,
// not on every step of a slider drag. Use it for simulations that take more
// than a fraction of a second:
//   viewof n = debounce(Inputs.range([20, 400], {value: 100, label: "n"}))
// The control's own display (the number box next to a slider) still updates
// immediately; OJS sees the new value `wait` milliseconds after the last change.
export function debounce(input, wait = 300) {
  let timer = null, passing = false;
  input.addEventListener("input", (event) => {
    if (passing) return;
    event.stopImmediatePropagation();
    clearTimeout(timer);
    timer = setTimeout(() => {
      passing = true;
      input.dispatchEvent(new Event("input", { bubbles: true }));
      passing = false;
    }, wait);
  });
  return input;
}
