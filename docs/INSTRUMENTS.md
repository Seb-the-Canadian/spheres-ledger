# Instruments

The fixed vocabulary for `instrument_family` and `instrument_class`: the
mechanisms an actor uses to constrain others.

This file and `data/instruments.csv` are the authority. Do not add a new
instrument class on the spot. Add one only if:

- it appears at least twice in the recorded events, **or**
- a primary document introduces a clearly new mechanism,

**and** you update this file, `data/instruments.csv` and `CHANGELOG.md` together.

---

## Spheres (for reference)

| Value | Name |
|---|---|
| `S1_Security` | Security |
| `S2_Finance` | Finance (sanctions, and permission over investment and ownership) |
| `S3_Trade` | Trade (tariffs, border enforcement, trade remedies) |
| `S4_Energy_Logistics` | Energy and Logistics (shipping, insurance and ports; price caps) |
| `S5_Tech_Compute` | Tech and Compute (export controls, licensing, cloud and platform access) |
| `S6_Legitimacy` | Legitimacy and Diplomatic (UN Security Council, recognition, bloc alignment) |

---

## Design rules

1. **Two levels.**
   - `instrument_family` is the broad bucket: a small, stable set.
   - `instrument_class` is the precise mechanism: still fixed, but more
     specific.
2. **One instrument per event.**
   - Every event picks exactly one `instrument_family` and one
     `instrument_class`.
   - If an event uses several mechanisms, split it into several events when the
     mechanisms can be analysed separately (preferred). Otherwise, describe them
     in `notes`.
3. **Keep it small.** Avoid splitting too finely. Aim for 20 to 40 classes in
   all.

---

## Families and classes

In `data/instruments.csv`, the family value is the code and name together, for
example `F1 kinetic_force`. The default sphere is a convenience only: each event
still states its own sphere.

### F1 kinetic_force

| Class | Default sphere | Definition |
|---|---|---|
| `kinetic_strike` | `S1_Security` | Use of force (air, missile or ground strike) with military intent. |
| `strike_and_capture` | `S1_Security` | Force applied with the detention or capture of leaders or personnel. |
| `raid_or_seizure` | `S1_Security` | A limited operation to seize assets or people, without being framed as a wider campaign. |

### F2 access_denial

| Class | Default sphere | Definition |
|---|---|---|
| `airspace_or_overflight_denial` | `S1_Security` | Denial of air transit rights, or closure announcements backed by signs of enforcement. |
| `basing_or_transit_denial` | `S1_Security` | Refusal or withdrawal of basing, refuelling or transit permission. |
| `port_access_denial` | `S4_Energy_Logistics` | Denial of port entry or servicing. Also usable in `S1_Security` when the logic is military transit denial. |

### F3 security_assistance

| Class | Default sphere | Definition |
|---|---|---|
| `security_assistance_halt` | `S1_Security` | Explicit withholding or stopping of arms, aid, intelligence and surveillance support, or training. |
| `security_assistance_release` | `S1_Security` | Explicit release or approval of arms, aid, intelligence and surveillance support, or training. |

### F4 sanctions_financial

| Class | Default sphere | Definition |
|---|---|---|
| `sanctions_designation` | `S2_Finance` | Listing or designation on a sanctions list, asset freezes, bans on transactions. |
| `secondary_sanctions` | `S2_Finance` | Sanctions threatened or applied against third parties for dealing with the target. |

### F5 investment_permissioning

| Class | Default sphere | Definition |
|---|---|---|
| `outbound_investment_restriction` | `S2_Finance` | Bans, notification duties or conditions on outbound investment in covered sectors. |
| `FDI_screening_framework` | `S2_Finance` | Mandatory or expanded screening of inbound investment, at bloc or national level. |
| `forced_divestment_or_unwind` | `S2_Finance` | A compelled sale or unwinding of ownership. |

### F6 tariffs_and_border

| Class | Default sphere | Definition |
|---|---|---|
| `tariff_rate_increase` | `S3_Trade` | A higher tariff rate on existing tariff lines. |
| `tariff_new_sector` | `S3_Trade` | A new tariff action on a sector not covered before, or a major expansion. |
| `quota_or_TRQ` | `S3_Trade` | A quota or tariff-rate quota put in place or changed. |
| `import_export_ban` | `S3_Trade` | An explicit ban on imports or exports. |
| `rules_of_origin_crackdown` | `S3_Trade` | Tighter checks on where goods come from, or enforcement against getting around trade measures. |

### F7 trade_remedies

| Class | Default sphere | Definition |
|---|---|---|
| `AD_CVD_provisional` | `S3_Trade` | Provisional anti-dumping or countervailing duties. |
| `AD_CVD_definitive` | `S3_Trade` | Definitive duties adopted, typically for several years. |
| `safeguard_measure` | `S3_Trade` | A temporary safeguard action. |

### F8 energy_logistics_controls

| Class | Default sphere | Definition |
|---|---|---|
| `oil_price_cap_dynamic` | `S4_Energy_Logistics` | A price cap with a moving formula or adjustment rule. |
| `shipping_insurance_restriction` | `S4_Energy_Logistics` | Restrictions on shipping insurance or services, tied to compliance. |
| `tanker_seizure_or_interdiction` | `S4_Energy_Logistics` | Physical interdiction or seizure of a vessel or cargo. |
| `energy_import_ban` | `S4_Energy_Logistics` | A ban on importing specific energy commodities or products. It may be phased in, with staggered compliance deadlines. Distinct from shipping and insurance restrictions: it applies to the commodity itself. |

### F9 export_controls

| Class | Default sphere | Definition |
|---|---|---|
| `export_control_global_tiering` | `S5_Tech_Compute` | A tiered global access framework: caps or blocks by category of destination. |
| `export_control_annual_license` | `S5_Tech_Compute` | Licensing or approval renewed each year, replacing standing waivers. |
| `shipment_hold_or_license_denial` | `S5_Tech_Compute` | A reported denial or hold of specific shipments or licences. |

### F10 platform_service_gating

| Class | Default sphere | Definition |
|---|---|---|
| `cloud_API_denial` | `S5_Tech_Compute` | Denial or throttling of access to cloud, API or model endpoints. |
| `vendor_support_cutoff` | `S5_Tech_Compute` | Ending vendor support, updates or maintenance. |
| `standards_cert_exclusion` | `S5_Tech_Compute` | Exclusion through standards, certification or interoperability requirements. |

### F11 policy_reversal

A meta tag. Use it with the sphere of the policy being reversed; the default
sphere in `data/instruments.csv` is only a convenience.

| Class | Default sphere | Definition |
|---|---|---|
| `rule_rescission_or_pause` | `S5_Tech_Compute` | Rescinds or pauses an earlier rule. This is a change of direction, not a loss of capacity. |
| `court_compelled_rescission` | `S3_Trade` | A court ruling that forces an earlier executive or regulatory action to end. Different from a rescission the executive chooses: the controller loses the instrument through an outside constraint, not by policy choice. |

A possible future split: if conditional relaxations (for example, moving from a
presumption of denial to case-by-case review) reach two or more cases, consider
giving them their own class, such as `conditional_review_relaxation`.

### F12 recognition_action

| Class | Default sphere | Definition |
|---|---|---|
| `recognition_grant_or_extension` | `S6_Legitimacy` | Formal recognition of a state or government, or extending existing recognition to a new territory or claim. |
| `recognition_withdrawal_or_denial` | `S6_Legitimacy` | Withdrawing existing recognition, or refusing to recognise a claim or government. |
| `ambassador_expulsion_or_recall` | `S6_Legitimacy` | Expelling or recalling ambassadors as a coercive signal. |

### F13 multilateral_governance_action

| Class | Default sphere | Definition |
|---|---|---|
| `UNSC_binding_resolution` | `S6_Legitimacy` | A UN Security Council resolution under Chapter VII that creates binding obligations. |
| `UNSC_veto_as_instrument` | `S6_Legitimacy` | Deliberate use of a veto to shield a target from a binding constraint. |

For `UNSC_veto_as_instrument`, C3 Net effect is counterfactual by nature: the
binding constraint was blocked, not imposed. Code the edge's role as
`controller` over the shielded resident's exposure to the Security Council.

---

## Changing the vocabulary

When you add a new `instrument_class`, also update:

- `data/instruments.csv`: its definition and default sphere;
- `CHANGELOG.md`: the version bump and the reason for it.
