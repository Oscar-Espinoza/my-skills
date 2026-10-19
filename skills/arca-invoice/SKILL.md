---
name: arca-invoice
description: "Prepare or issue Oscar's monthly Go Nimbly export invoice through ARCA's Comprobantes en Línea portal. Use for requests to invoice a service month, create a Factura E, or resume this personal invoicing process across AI providers."
---

# ARCA monthly invoice

Create the requested monthly invoice without depending on the original chat.
Use the browser tools available in the current harness; no particular extension,
model or browser session is required. If browser control is unavailable, prepare
the fields and guide the user, clearly stating that no invoice was issued.

## Load the current private records

Source of truth for billing instructions and invoice history:
**https://github.com/Oscar-Espinoza/arca-invoicing** (private).

Read the current `START-HERE.md`, `BILLING.md` and `INVOICES.md` from that
repository before preparing an invoice. Prefer the user's existing checkout or
connected GitHub access. On Oscar's original PC the checkout is
`~/Projects/arca-invoicing`; on another machine obtain the private repository
through the user's authorized access. If unavailable, ask for access or these
three files. Never make the repository public. Do not assume the local contract,
certificates or saved browser sessions exist on another machine.

Keep billing details in that repository rather than copying a second profile
into this skill. At creation the arrangement was Go Nimbly, US$3,000 per full
month, month-end, net 30, paid in USD. Those are orientation only: use the current
profile and current user instructions, especially for raises or partial months.

## Perform the requested operation

1. Establish the service month and whether the user wants a draft or issuance.
   Ask only for missing or conflicting information that changes the invoice.
   A draft request does not authorize issuance; an explicit request to create
   or issue the invoice within the stated details does.
2. Open ARCA's official Clave Fiscal portal and let the user authenticate:
   https://auth.afip.gob.ar/contribuyente/. Use the tab the user identifies,
   regardless of its number. Never request their password in chat or save it.
3. Confirm issuer identity against `BILLING.md`. In Comprobantes en Línea,
   inspect issued invoices for the requested client/service month before
   creating one. A missing register entry is not proof of absence in ARCA.
4. Follow `START-HERE.md` using the current portal UI, with fresh observations
   rather than saved element IDs. Use the active web export point of sale;
   the documented one is 00005. Do not repurpose Web Services point 00007.
   Review recipient, service period, issue date, USD total, payment date,
   payment currency and ARCA's exchange-rate field. Do not invent an EIN or
   substitute an ARQ conversion rate.
5. Respect the requested service period and month-end arrangement. Do not issue
   early or silently backdate/catch up historical missing invoices. Resolve an
   unusual date or changed employment facts using current authoritative ARCA
   guidance. Do not treat an old plan as evidence of income actually earned.
6. Review the completed fields before submission. Stop before issuance for a
   draft. For authorized issuance, submit once and confirm acceptance. After a
   timeout or ambiguous result, query ARCA and reconcile; never blindly repeat.
7. Retrieve the official PDF if available, verify it, and update `INVOICES.md`
   with service month, issue date, point/number, USD total, CAE/expiry and receipt
   location. Preserve existing rows. If the shared register cannot be updated,
   tell the user and supply the record to save. Report only observed results.

## Preserve the user's operating choice

Cloud and local schedulers were disabled at the user's request on October 19,
2026. Leave them disabled unless the user requests a change. Real invoicing is
on request through the web portal. WSASS test-certificate failures block the
custom API test, not the web invoicing route. Do not silently use the custom API
or bypass its unresolved test requirement.

If specifically asked to retry the API test, read the invoicing repository's
README and run its resumable `./retry-test` command where available. Distinguish
login needed, ARCA server failure and an actual accepted-and-retrieved test
invoice. The command is a manual trigger, not an unattended monitor.

Do not change tax registration, pay taxes/debts, correct past invoices or send
the invoice to Go Nimbly without the user's request. Keep private keys, tokens,
session cookies and passwords out of Git, documents, logs and chat. Keep official
receipts and billing records private.
