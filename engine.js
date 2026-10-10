// Amigurumi math engine - pure arithmetic, shared by the page and the tests.
// Every borrowed number is a labeled craft norm, not a rule.
(function (root) {
"use strict";

// Labeled norms:
// - Safety eyes: about 1/6 of the head diameter (circumference / pi), placed about half a head diameter apart.
// - Stuffing: about 12 g of fiberfill per liter of toy, toy volume estimated as an ellipsoid (pi/6 x l x w x h).
var EYE_PART = 6;
var GAP_PART = 2;
var FILL_PER_L = 12;

function r1(x) { return Math.round(x * 10) / 10; }
function positive() {
  for (var i = 0; i < arguments.length; i++) {
    var v = arguments[i];
    if (typeof v !== "number" || !isFinite(v) || v <= 0) return false;
  }
  return true;
}

function eyeSize(headCm) {
  if (!positive(headCm)) return { error: "head size must be positive" };
  var diamMm = headCm * 10 / Math.PI;
  return {
    headCm: r1(headCm),
    headMm: r1(diamMm),
    eyeMm: r1(diamMm / EYE_PART),
    gapMm: r1(diamMm / GAP_PART)
  };
}

function renderEye(r) {
  if (r.error) return r.error;
  return "Head about " + r.headMm + " mm across - try " + r.eyeMm + " mm safety eyes, placed about " + r.gapMm +
    " mm apart (labeled ratios, your pattern wins).";
}

function stuffing(l, w, h) {
  if (!positive(l, w, h)) return { error: "toy dimensions must be positive" };
  var volMl = Math.PI / 6 * l * w * h;
  var grams = r1(volMl / 1000 * FILL_PER_L);
  return { volMl: r1(volMl), grams: grams };
}

function renderStuff(r) {
  if (r.error) return r.error;
  return "Toy volume about " + r.volMl + " ml - plan on " + r.grams + " g of fiberfill (labeled " +
    FILL_PER_L + " g per liter, ellipsoid estimate).";
}

function bagCount(toys, perToyG, bagG) {
  if (!positive(toys, perToyG, bagG)) return { error: "inputs must be positive" };
  var need = r1(toys * perToyG);
  var bags = Math.ceil(need / bagG);
  return { toys: toys, perToyG: r1(perToyG), need: need, bags: bags, leftover: r1(bags * bagG - need), bagG: r1(bagG) };
}

function renderBag(r) {
  if (r.error) return r.error;
  return r.toys + " toys at " + r.perToyG + " g each need " + r.need + " g - " + r.bags + " bag" +
    (r.bags === 1 ? "" : "s") + " of " + r.bagG + " g, leaving " + r.leftover + " g spare.";
}

var api = {
  eyeSize: eyeSize,
  stuffing: stuffing,
  bagCount: bagCount,
  renderEye: renderEye,
  renderStuff: renderStuff,
  renderBag: renderBag
};
if (typeof module !== "undefined" && module.exports) module.exports = api;
root.AmigurumiMath = api;
})(typeof window !== "undefined" ? window : globalThis);
