const CATALOGUE = [{"id": "SWIM-01", "name": "Little Ripples Beginner Swim", "interest": "swimming", "minAgeYears": 4, "maxAgeYears": 6, "priceSGD": 40, "district": "Bukit Timah", "level": "beginner", "availability": "unverified", "source": "Fictional learning catalogue", "revision": "v1"}, {"id": "SWIM-02", "name": "Junior Swim Squad", "interest": "swimming", "minAgeYears": 8, "maxAgeYears": 12, "priceSGD": 35, "district": "Bukit Timah", "level": "advanced", "availability": "unverified", "source": "Fictional learning catalogue", "revision": "v1"}, {"id": "SWIM-03", "name": "Small Splash Premium", "interest": "swimming", "minAgeYears": 4, "maxAgeYears": 6, "priceSGD": 65, "district": "Bukit Timah", "level": "beginner", "availability": "unverified", "source": "Fictional learning catalogue", "revision": "v1"}, {"id": "ART-01", "name": "Messy Colours Studio", "interest": "art", "minAgeYears": 4, "maxAgeYears": 7, "priceSGD": 38, "district": "Bukit Timah", "level": "beginner", "availability": "unverified", "source": "Fictional learning catalogue", "revision": "v1"}, {"id": "ART-02", "name": "Eastside Creative Play", "interest": "art", "minAgeYears": 3, "maxAgeYears": 6, "priceSGD": 28, "district": "East", "level": "beginner", "availability": "unverified", "source": "Fictional learning catalogue", "revision": "v1"}, {"id": "OUTDOOR-01", "name": "Woodland Explorers", "interest": "outdoor", "minAgeYears": 5, "maxAgeYears": 9, "priceSGD": 45, "district": "Bukit Timah", "level": "beginner", "availability": "unverified", "source": "Fictional learning catalogue", "revision": "v1"}, {"id": "ART-03", "name": "Mystery Price Art", "interest": "art", "minAgeYears": 4, "maxAgeYears": 7, "priceSGD": null, "district": "Bukit Timah", "level": "beginner", "availability": "unverified", "source": "Fictional learning catalogue", "revision": "v1"}];
// n8n Code node, JavaScript, Run Once for All Items. Fictional read-only data.
const input = $input.first()?.json ?? {};
const missing = x => x === null || x === undefined || String(x).trim() === "";
const age = missing(input.ageYears) ? NaN : Number(input.ageYears);
const budget = missing(input.budgetMaxSGD) ? NaN : Number(input.budgetMaxSGD);
if (!Number.isFinite(age) || age < 0 || age > 18 || !Number.isFinite(budget) || budget < 0 || budget > 10000) {
  return [{json:{status:"invalid_input",message:"Supply age in years (0–18) and maximum SGD budget (0–10000)."}}];
}
const rawInterest = String(input.interest ?? "any").trim().toLowerCase();
const synonyms = {swim:"swimming",swimming:"swimming",art:"art",creative:"art",outdoor:"outdoor",nature:"outdoor",any:"any"};
const interest = synonyms[rawInterest];
const rawDistrict = String(input.district ?? "any").trim().toLowerCase();
const districts = {any:"any","bukit timah":"Bukit Timah",east:"East"};
const district = districts[rawDistrict];
if (!interest || !district) return [{json:{status:"invalid_input",message:"Use a supported interest (swimming/art/outdoor/any) and area (Bukit Timah/East/any). Ask the parent before broadening."}}];
const matches = CATALOGUE.filter(a => age >= a.minAgeYears && age <= a.maxAgeYears &&
 a.priceSGD !== null && a.priceSGD <= budget && (interest === "any" || a.interest === interest) &&
 (district === "any" || a.district === district)).slice(0,10);
return [{json:{status:matches.length?"success":"no_matches",matches,availabilityVerified:false,
 note:"Fictional records. A match is not verified availability or a booking. Blank prices are excluded under a strict budget."}}];
