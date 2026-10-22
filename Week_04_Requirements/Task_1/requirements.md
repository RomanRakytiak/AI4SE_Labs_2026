# Refined Software Requirements

## Priority Scale

- **Critical**: Required for the system to be viable or safe.
- **High**: Important for the primary workflow; omission causes major impact.
- **Medium**: Valuable requirement that can follow the primary workflow.
- **Low**: Useful enhancement with limited impact if deferred.

## Requirements

### REQ-001: Material volume report by library at a point in time

**Priority:** High

**Derived from:**
- `conversations/conv_pines014_material_volume.eml`

The system shall provide a report showing the volume of material for a specified library at any point in time.

### REQ-002: Volume totals with category breakdowns

**Priority:** High

**Derived from:**
- `conversations/conv_pines014_material_volume.eml`

The volume report shall show total item counts in the library and break volume down by categories. The category set and category definitions are not specified, so the reporting must work with an unresolved category taxonomy/definition source.

### REQ-003: Volume by material state (acquisitions, on-shelf, in-circulation)

**Priority:** High

**Derived from:**
- `conversations/conv_pines014_material_volume.eml`

The volume report shall separately report new acquisitions, items on the shelf (checked in), and items out in circulation (checked out), and also provide an overall total. It is unresolved whether “new acquisitions” is mutually exclusive from the other states or may overlap, so the state semantics remain to be clarified.

### REQ-004: Library-configurable report categories for volume breakdowns

**Priority:** Medium

**Derived from:**
- `conversations/conv_pines014_material_volume.eml`

The volume report shall support library-configurable categories used for breaking down material volume. The mechanism and scope of category configuration are unspecified, and must be determined later.

### REQ-005: Holds counts included in volume category breakdowns

**Priority:** Medium

**Derived from:**
- `conversations/conv_pines014_material_volume.eml`

The volume report shall include the number of holds, including holds counts within the category breakdowns. It is unresolved how a hold is counted (e.g., item versus transaction versus another measure) and how multiple holds are aggregated.

### REQ-006: Historical volume filtering with date filters

**Priority:** High

**Derived from:**
- `conversations/conv_pines014_material_volume.eml`

The volume report shall support date filters so it can report volume at points in time and compare historical volume changes. Applicable date semantics and supported date ranges are not specified.

### REQ-007: Acquisition-date reporting for volume added over time

**Priority:** Medium

**Derived from:**
- `conversations/conv_pines014_material_volume.eml`

The system shall use item acquisition dates to report how much volume was added over time. It is unresolved whether standard reporting periods (e.g., 30/60/90 days) are required or only examples.

### REQ-008: All-branch capacity overview interface

**Priority:** High

**Derived from:**
- `conversations/conv_pines015_capacity_interface.eml`

The system shall provide a high-level interface showing the capacity of all branches at once. The meaning and metrics of “capacity” are not defined, so the underlying capacity definition remains unresolved.

### REQ-009: Branch capacity drill-down

**Priority:** Medium

**Derived from:**
- `conversations/conv_pines015_capacity_interface.eml`

The capacity interface shall allow users to drill down into an individual branch’s capacity. The specific detail fields and presentation for the drilled-down view are unspecified.

### REQ-010: Sort and filter branch capacity by region, type, and current load

**Priority:** Medium

**Derived from:**
- `conversations/conv_pines015_capacity_interface.eml`

The capacity interface shall support sorting and filtering branch capacity information by region, branch type, and current load. The available branch types and the definition of “current load” are not specified.

### REQ-011: Capacity trend data over time

**Priority:** Medium

**Derived from:**
- `conversations/conv_pines015_capacity_interface.eml`

The capacity interface shall provide trend data indicating branch growth or shrink patterns over time. The time range, granularity, and calculation method are not specified.

### REQ-012: CSV export for capacity information

**Priority:** Low

**Derived from:**
- `conversations/conv_pines015_capacity_interface.eml`

The system shall allow capacity information to be exported to CSV. The export scope and included fields are unspecified.

### REQ-013: Usability constraint for 286-location capacity overview

**Priority:** Medium

**Derived from:**
- `conversations/conv_pines015_capacity_interface.eml`

The capacity interface design must account for displaying an overview of 286 locations without making the overview unusably crowded. No measurable usability threshold or required mitigation (e.g., grouping/filtering rules) is defined.

### REQ-014: Shelf space usage report comparing circulations, collection, and shelf space by genre/format

**Priority:** High

**Derived from:**
- `conversations/conv_pines016_shelf_space.eml`

The system shall provide a report for each genre and format of material that compares the percentage of total circulations, percentage of the collection, and percentage of total shelf space.

### REQ-015: Shelf space usage report at library and system scopes

**Priority:** High

**Derived from:**
- `conversations/conv_pines016_shelf_space.eml`

The shelf space report shall be available at both the individual-library level and the system level.

### REQ-016: Compute percentage of collection by counting items per genre/format

**Priority:** High

**Derived from:**
- `conversations/conv_pines016_shelf_space.eml`

The “percentage of collection” metric shall be based on counting items by genre and format.

### REQ-017: Compute percentage of circulations by summing checkouts per genre/format

**Priority:** High

**Derived from:**
- `conversations/conv_pines016_shelf_space.eml`

The “percentage of total circulations” metric shall be based on summing checkouts by genre and format.

### REQ-018: Unresolved: shelf space measurement estimation basis

**Priority:** High

**Derived from:**
- `conversations/conv_pines016_shelf_space.eml`

The system must determine or support a defined method for estimating shelf space by genre and format because shelf space is not directly tracked in the database. The source mentions possible approaches (estimating from item dimensions or using item count as a proxy) but does not select or define estimation rules.

### REQ-019: Select transfer candidates via saved queries and manual title selection

**Priority:** High

**Derived from:**
- `conversations/conv_pines018_item_transfer.eml`
- `interview_cataloging_2009-05-08.txt`

The item transfer utility shall query for candidate materials, save queries for repeated use, and allow staff to manually select titles from query results.

### REQ-020: Execute batch transfers with location changes and pull-list generation

**Priority:** High

**Derived from:**
- `conversations/conv_pines018_item_transfer.eml`

The item transfer utility shall transfer selected items between branches by changing their location records and supporting pull-list generation.

### REQ-021: Automatically revert transferred items after a period and/or criteria

**Priority:** High

**Derived from:**
- `conversations/conv_pines018_item_transfer.eml`

The item transfer utility shall revert transferred items to their original location after a specified period and/or when configured criteria are met, including time- or status-based criteria. The allowable criteria set and precedence when multiple criteria apply are not defined.

### REQ-022: Protect transfer actions with role restrictions, preview, and undo

**Priority:** High

**Derived from:**
- `conversations/conv_pines018_item_transfer.eml`

The item transfer utility shall restrict transfer permissions to designated roles, show a preview before applying changes, and provide an undo function. The exact authorized roles and undo scope/retention period are not defined.

### REQ-023: Maintain transfer history for items

**Priority:** Medium

**Derived from:**
- `conversations/conv_pines018_item_transfer.eml`

The system shall maintain transfer history for items, including information that supports determining how often an item has been transferred. Required history fields and retention period are not defined.

### REQ-024: Generate printable transit labels/barcodes for transfers

**Priority:** Medium

**Derived from:**
- `conversations/conv_pines018_item_transfer.eml`

The item transfer utility shall generate printable transit labels or barcodes for items being transferred. The label format and required barcode content are not defined.

### REQ-025: Alert staff when transfer is delayed or has issues

**Priority:** Low

**Derived from:**
- `conversations/conv_pines018_item_transfer.eml`

The item transfer utility shall provide alerts when an item transfer is delayed or has issues. Delay thresholds, issue types, recipients, and notification channels are not defined.

### REQ-026: Non-functional: scalable batch processing without database locking problems

**Priority:** High

**Derived from:**
- `conversations/conv_pines018_item_transfer.eml`

Batch transfer processing shall remain efficient for approximately 9.6 million items and avoid database locking problems. No measurable performance targets or concurrency limits are specified.

### REQ-027: Missing and damaged items report grouped per branch

**Priority:** High

**Derived from:**
- `conversations/conv_pines019_020_missing_intransit.eml`
- `interview_cataloging_2009-05-08.txt`

The system shall provide reports of missing and damaged items grouped per branch.

### REQ-028: In-transit report for items exceeding configurable days threshold

**Priority:** High

**Derived from:**
- `conversations/conv_pines019_020_missing_intransit.eml`
- `interview_cataloging_2009-05-08.txt`

The system shall generate a report of items that have been in transit for more than a configurable threshold X days, scoped per branch and per system. A default of 7 days was suggested but not confirmed; semantics of transit start date are also unspecified in the sources.

### REQ-029: Unified transit-direction report combining transit-to and transit-from

**Priority:** High

**Derived from:**
- `conversations/conv_pines019_020_missing_intransit.eml`
- `interview_cataloging_2009-05-08.txt`

The in-transit report shall combine transit-to and transit-from items into one report.

### REQ-030: Identify purge candidates using customizable status/time/activity/combined criteria

**Priority:** High

**Derived from:**
- `conversations/conv_pines021_item_purging.eml`

The system shall provide a utility and reports that identify item records for purging using customizable status-based, time-based, activity-based, and combined criteria. The supported criteria syntax, operators, and precedence are not specified.

### REQ-031: Batch conversion of item status from one value to another

**Priority:** Medium

**Derived from:**
- `conversations/conv_pines021_item_purging.eml`
- `interview_cataloging_2009-05-08.txt`

The system shall provide a report or workflow to assist with converting multiple items from one status to another in batch. It is unresolved whether the workflow itself performs conversion or only identifies items for a separate action.

### REQ-032: Last copy report for only-copy flags in a specified scope

**Priority:** High

**Derived from:**
- `conversations/conv_pines021_item_purging.eml`
- `interview_cataloging_2009-05-08.txt`

The system shall provide a last copy report that flags item records that are the only copy within a specified scope, including library and entire consortium/system scopes. The source uses multiple scope wordings (“library system” and “entire PINES system”), and exact scope definitions and selectable views require clarification.

### REQ-033: Quick cleanup to delete volume entries with copies and delete orphan records

**Priority:** High

**Derived from:**
- `conversations/conv_pines021_item_purging.eml`
- `interview_cataloging_2009-05-08.txt`

The system shall provide a quick, effective method to delete volume entries together with their copy entries, and to delete records with no items attached. The source does not specify whether the operation is automated versus manual or what audit/confirmation controls apply.

### REQ-034: Purge candidate identification reports are read-only

**Priority:** High

**Derived from:**
- `conversations/conv_pines021_item_purging.eml`

Reports that identify candidates for purging shall be read-only and shall not directly delete records.

### REQ-035: Require separate confirmation step for actual deletions

**Priority:** High

**Derived from:**
- `conversations/conv_pines021_item_purging.eml`

Actual deletions shall require a separate confirmation step after candidate identification. The confirmation mechanism and authorization requirements are not defined.

### REQ-036: Purge audit trail records who purged what and when

**Priority:** High

**Derived from:**
- `conversations/conv_pines021_item_purging.eml`

The system shall maintain an audit trail for all purges, including who purged what and when. Retention, visibility, and immutability requirements are not specified.

### REQ-037: Deletion audit logging includes record type, timestamp, user, and user location

**Priority:** High

**Derived from:**
- `conversations/conv_pines022_deletions.eml`
- `interview_cataloging_2009-05-08.txt`

The system shall record and track deletions of records, including the record type, deletion timestamp, user who performed the deletion, and the user's location.

### REQ-038: Deletion counts tracked by location and system

**Priority:** Medium

**Derived from:**
- `conversations/conv_pines022_deletions.eml`
- `interview_cataloging_2009-05-08.txt`

The system shall count and track record deletions by location and by system.

### REQ-039: Deletion reporting with queryable breakdowns

**Priority:** Medium

**Derived from:**
- `conversations/conv_pines022_deletions.eml`

The system shall provide reports that allow users to query deletion audit data and view deletion totals and breakdowns by time period, record type, location, and deleting user.

### REQ-040: Periodic deletion summaries (month, quarter, year)

**Priority:** Low

**Derived from:**
- `conversations/conv_pines022_deletions.eml`

The system shall report total deletions for month, quarter, and year periods.

### REQ-041: Deletion activity ranking by user

**Priority:** Low

**Derived from:**
- `conversations/conv_pines022_deletions.eml`

The system shall report which users delete the most records.

### REQ-042: Patron characteristic queries and grouping

**Priority:** High

**Derived from:**
- `conversations/conv_pines023_patron_characteristics.eml`

The system shall allow queries and reports to be limited or grouped by age range, zip code, county of residence, home branch, patron type, and preferred language.

### REQ-043: Combine patron characteristic filters with AND/OR logic

**Priority:** High

**Derived from:**
- `conversations/conv_pines023_patron_characteristics.eml`

The system shall support combining patron-characteristic filters using AND and OR logic.

### REQ-044: Configurable age ranges per report

**Priority:** Medium

**Derived from:**
- `conversations/conv_pines023_patron_characteristics.eml`

The system shall allow age ranges to be configured per report. Validation rules for overlapping, discontinuous, or invalid age ranges are not specified.

### REQ-045: Include patrons with missing optional characteristic values (nulls)

**Priority:** Medium

**Derived from:**
- `conversations/conv_pines023_patron_characteristics.eml`

Reports shall include patrons whose optional characteristic fields are missing, displaying null values rather than excluding those records. Presentation/labeling of null values is not specified.

### REQ-046: Inactive patrons report for configurable X days with no circulation or electronic activity

**Priority:** High

**Derived from:**
- `conversations/conv_pines024_inactive_patrons.eml`

The system shall generate a list of patrons with no circulation or electronic activity during the preceding configurable number of days X. The allowable range and treatment of patrons with no recorded activity are not specified.

### REQ-047: Electronic activity definition for inactive patron determination

**Priority:** High

**Derived from:**
- `conversations/conv_pines024_inactive_patrons.eml`

For inactive-patron determination, electronic activity shall include OPAC or patron-account logins, online hold placements, and online renewals; access to digital collections may also count when integrated. The consolidated requirement is ambiguous about whether digital-resource access is included by default and how inclusion is determined.

### REQ-048: Inactive patrons configurable aggregation/listing scope levels

**Priority:** Medium

**Derived from:**
- `conversations/conv_pines024_inactive_patrons.eml`

The inactive-patron report shall support configurable aggregation or listing levels including System, Home Library, and County, with other levels permitted as needed. Available levels, access rules, and meaning of “other levels as needed” are not defined.

### REQ-049: Inactive patrons report includes current mailing addresses

**Priority:** Medium

**Derived from:**
- `conversations/conv_pines024_inactive_patrons.eml`

The inactive-patron report shall include patrons' current mailing addresses for outreach. Required address fields and handling for patrons without a current address are unspecified.

### REQ-050: Inactive patrons with outstanding fines tracked separately

**Priority:** Medium

**Derived from:**
- `conversations/conv_pines024_inactive_patrons.eml`

The system shall track inactive patrons with outstanding fines separately from other inactive patrons. The separate output or handling process is not defined.

### REQ-051: Exclude certain patron types from inactive-patron report

**Priority:** Medium

**Derived from:**
- `conversations/conv_pines024_inactive_patrons.eml`

The system shall allow certain patron types to be excluded from the inactive-patron report. The configuration mechanism and authoritative patron-type flags are not specified.

### REQ-052: Inactive-patrons report CSV export

**Priority:** Low

**Derived from:**
- `conversations/conv_pines024_inactive_patrons.eml`

The inactive-patron report shall be exportable in CSV format.

### REQ-053: Non-functional: background report processing for inactive patrons

**Priority:** Medium

**Derived from:**
- `conversations/conv_pines024_inactive_patrons.eml`

The inactive-patron report shall run as a background process to support performance for large patron populations. No performance target, scheduling behavior, completion notification, or result-retention requirement is specified.

### REQ-054: Support consortium scale, Linux/Solaris, and assistive technologies (unmeasured)

**Priority:** High

**Derived from:**
- `early_draft_srs_galecia.txt`

The system must support a library consortium with 286 locations and 17 million annual circulations, operate on Linux or Solaris, and be accessible through a web browser or a Windows-compatible client while supporting assistive technologies such as screen readers and screen magnification software. Measurable performance and specific legacy browser version requirements are not defined in the source.

### REQ-055: Role-based access and fine-grained report permissions (creation/cloning/execution/sharing/fields)

**Priority:** High

**Derived from:**
- `early_draft_srs_galecia.txt`

The system must control access through security groups or roles and provide fine-grained permissions for report creation, cloning, execution, shared folders, tables, and fields. The permission model, role administration process, and precedence between restrictions are unspecified.

### REQ-056: Query and reporting tools across bibliographic/item/patron/transaction/financial records

**Priority:** High

**Derived from:**
- `early_draft_srs_galecia.txt`

The system must provide query and reporting tools covering bibliographic, item, patron, transaction, and financial records, with selectable fields, value selection including regular expressions, Boolean operators, and configurable report templates or interfaces. Record schema and query semantics/validation behavior are not defined.

### REQ-057: Immediate, recurring, and scheduled report execution with queue visibility and email delivery

**Priority:** High

**Derived from:**
- `early_draft_srs_galecia.txt`

The system must support immediate, recurring, and scheduled reports, including report queue visibility, cancellation, prioritization, configurable output formats, and delivery to email addresses. Scheduling guarantees, email security, output fidelity, and failure handling are unspecified.

### REQ-058: Retain transaction history and support real-time and historical reporting by date

**Priority:** High

**Derived from:**
- `early_draft_srs_galecia.txt`

The system must retain detailed transaction history for a configurable period, retain monthly and annual aggregates indefinitely, and support real-time and historical reporting for specified dates or date ranges. The value/minimum bounds of the history period, definitions of real time, historical warehouse retention, and historical correction rules are unspecified.

### REQ-059: Privacy-preserving transaction archiving and demographic analytics

**Priority:** High

**Derived from:**
- `early_draft_srs_galecia.txt`

The system must archive transactions and produce demographic statistics while removing or protecting information that could identify patrons in accordance with applicable state privacy law. Applicable law, anonymization method, re-identification controls, retention exceptions, and authorized access rules are not specified.

### REQ-060: Inventory and item lifecycle management analytics with transfers, reports, conversions, and purging

**Priority:** High

**Derived from:**
- `early_draft_srs_galecia.txt`

The system must support inventory analysis and control across branches, including capacity and shelf-space reporting, uncataloged material tracking, batch item transfers with saved queries and reversible location changes, missing/damaged reports, and configurable item status conversion or purging. The source lists capabilities but leaves authorization, transactional integrity, conflict handling, reversal behavior after edits, and safeguards for destructive purging undefined.

### REQ-061: Transaction, patron, and financial reporting with specified dimensions

**Priority:** High

**Derived from:**
- `early_draft_srs_galecia.txt`

The system must report and aggregate circulation, holds, patron characteristics, fines, charges, waivers, payments, item values, and financial audit data by specified dimensions (patron, branch, system, geographic, time, and transaction). Many terms and definitions of counts and aggregation rules are not fully specified.

### REQ-062: Developer provides data specifications and online hierarchical cross-linked HTML help

**Priority:** Medium

**Derived from:**
- `early_draft_srs_galecia.txt`

The developer must provide complete record data specifications, high-level process descriptions, and an online hierarchical, cross-linked HTML help system covering all system functions, along with thorough administrator-facing error and query feedback. Completeness, update/version obligations, accessibility of documentation, and meaning of low-level query feedback are undefined.

### REQ-063: Item value reports aggregating item-record value by scope

**Priority:** High

**Derived from:**
- `email_financial_reports.eml`

The system shall generate reports aggregating item values from item-record data for the entire collection or for a selected portion.

### REQ-064: Financial reports: balances, fines/charges/waivers, and payments

**Priority:** High

**Derived from:**
- `email_financial_reports.eml`

The system shall provide financial reports including patron account balances by patron, home library, and system; fines and charges by time period and charge type; fines waived by time period and branch; and payments by time period, payment method, and library or collection location. The relationship between payment methods and collection channels is not defined in the source.

### REQ-065: Query patron accounts by balance threshold

**Priority:** Medium

**Derived from:**
- `email_financial_reports.eml`

Staff shall be able to query patron accounts whose balances exceed a specified dollar threshold. The meaning of the threshold value, supported comparison operators, and the definition of balance are not specified.

### REQ-066: Maintain payment audit ledger mapping payments to applied charges

**Priority:** High

**Derived from:**
- `email_financial_reports.eml`

The system shall maintain a ledger of patron payments that identifies the specific charges to which each payment was applied, supporting reconciliation.

### REQ-067: Reports and archived data comply with auditing requirements

**Priority:** High

**Derived from:**
- `email_financial_reports.eml`

Reports and archived data shall comply with standard accounting practice and applicable state, county, and municipal auditing requirements. Applicable standards/jurisdictions and measurable compliance criteria are not identified.

### REQ-068: Enforce financial data retention policies (seven-year retention where required)

**Priority:** High

**Derived from:**
- `email_financial_reports.eml`

The system shall enforce data-retention policies for archived financial data, including a seven-year retention period where required for audit purposes. The data subject to seven-year retention, policy exceptions, and disposal rules are unspecified.

### REQ-069: Join patron-associated and item-associated financial data for reporting

**Priority:** High

**Derived from:**
- `email_financial_reports.eml`

The system shall support financial information associated with both patron records and item records and allow these data sources to be joined for financial reporting.

### REQ-070: Financial information updates promptly when transactions occur

**Priority:** Medium

**Derived from:**
- `email_financial_reports.eml`

The system shall allow financial information to be updated promptly when transactions such as front-desk payments occur. The required update time and scope of what must update immediately are not specified.

### REQ-071: User-friendly query design interface for all record types

**Priority:** High

**Derived from:**
- `email_report_features.eml`

The system shall provide a user-friendly query-design interface for all record types, allowing users to select query fields, choose picklist values, select regular expressions from a dropdown, and combine criteria with Boolean operators.

### REQ-072: Show query criteria/selection values with results

**Priority:** Medium

**Derived from:**
- `email_report_features.eml`

The system shall provide the query selections or criteria together with the query results.

### REQ-073: Report template management with run/modify limits and cloning

**Priority:** High

**Derived from:**
- `email_report_features.eml`

Administrators shall be able to create report templates that staff can access and run unchanged or modify within administrator-defined limits on alterable filters and display fields. Users shall also be able to clone an existing template into a new report variant while template use preserves consistent intended criteria and results. The exact limits and rules for modifications that do not compromise results are not defined.

### REQ-074: Report permissions and roles for create/clone/run and shared folders

**Priority:** High

**Derived from:**
- `email_report_features.eml`

The system shall support distinct, fine-grained permissions controlling who can create and clone reports, run specific shared reports, and run ad hoc reports against specific datasets. Administrators manage access through shared folders and role-based permissions that update automatically when a user's role changes. The permission model details are not fully specified.

### REQ-075: Predefined board/activity reports with required cross-tabulation dimensions

**Priority:** Medium

**Derived from:**
- `email_report_features.eml`

The system shall provide predefined reports for library boards, including basic statistics required for the Georgia Annual Report and activity measures (traffic/usage) such as checkouts, check-ins, holds placed, and holds filled. These reports shall support cross-tabulation by terminal, branch, system, hour, age range, patron type, and patron location. Specific Georgia Annual Report measures beyond the listed categories are not enumerated in the source.

### REQ-076: Transaction archive retains required history while protecting patron privacy

**Priority:** High

**Derived from:**
- `email_report_features.eml`

The system shall retain transaction data for the period required by state law while protecting patron privacy by not retaining personally identifiable information, and shall preserve sufficient data to produce useful demographic statistics. Retention period is expressed as “X years,” and anonymization/de-identification method are unspecified.

### REQ-077: Report queue visibility with status, submission time, and position

**Priority:** High

**Derived from:**
- `email_report_features.eml`
- `survey_results_2009.txt`
- `evergreen_reference_2009.txt`

The system shall show staff whether a submitted report is queued, how many reports are ahead of it, when it was submitted, and its status as waiting, running, completed, or failed.

### REQ-078: Report prioritization so important reports run ahead of others

**Priority:** Medium

**Derived from:**
- `email_report_features.eml`

The system shall support prioritizing reports so that authorized important reports (e.g., director board reports) can run ahead of lower-priority reports (e.g., staff ad hoc queries). The actors authorized to set priority and the priority rules/levels are not specified.

### REQ-079: Optional streamlined staff login methods (e.g., card swipe)

**Priority:** Medium

**Derived from:**
- `email_staff_login.eml`

The system shall support streamlined staff login methods such as card swipe, without requiring their use. The specific supported methods and deployment/configuration details are not defined.

### REQ-080: Support username/password staff authentication fallback

**Priority:** Medium

**Derived from:**
- `email_staff_login.eml`

The system shall support individual username-and-password login in addition to streamlined login methods. Password policy, recovery, and session behavior are unspecified.

### REQ-081: Authenticate and record the individual staff member for audit

**Priority:** High

**Derived from:**
- `email_staff_login.eml`

Regardless of login method, the system shall authenticate and identify the individual staff member who is logged in for audit purposes. The required audit records and retention period are not specified.

### REQ-082: Role-based access control using security groups or roles

**Priority:** High

**Derived from:**
- `email_staff_login.eml`

The system shall control user rights and privileges through assigned security groups or roles. The exact permission model and precedence when users have multiple roles are unspecified.

### REQ-083: Access control assignments for individuals, workgroups, and arbitrary groups

**Priority:** Medium

**Derived from:**
- `email_staff_login.eml`

The system shall support access control assignments for individual staff members, workgroups, and arbitrary staff groups. The structure and management of workgroups/arbitrary groups are unspecified.

### REQ-084: Administrator manages roles/security groups and updates permissions via role assignment

**Priority:** High

**Derived from:**
- `email_staff_login.eml`

Administrators shall be able to create and manage security groups or roles and change a staff member's permissions by changing the person's role assignment. “Easy/simple” is not measurable, and administrator scope is not defined.

### REQ-085: Track uncataloged materials as inventory and include transactions in circulation statistics

**Priority:** High

**Derived from:**
- `interview_cataloging_2009-05-08.txt`

The system shall track uncataloged materials as inventory, support rapid processing with minimal branch labor, identify material usage, and include their transactions in circulation statistics and reports.

### REQ-086: Reports for missing/damaged and in-transit items by branch and system

**Priority:** High

**Derived from:**
- `interview_cataloging_2009-05-08.txt`
- `conversations/conv_pines019_020_missing_intransit.eml`

The system shall provide reports of missing and damaged items by branch, and a combined in-transit report showing items in transit longer than a configurable number of days, scoped by branch and system. The meaning of the configurable X days and the definition of an item's transit start date are unspecified.

### REQ-087: Collection management analysis: shelf space usage and material volume reports

**Priority:** High

**Derived from:**
- `interview_cataloging_2009-05-08.txt`

The system shall provide a shelf space report comparing circulation percentage, collection percentage, and shelf-space percentage by genre and format, and a material volume report covering acquisitions, on-shelf items, and circulating items by category.

### REQ-088: Data quality reports and last item edit date excluding circulation activity

**Priority:** Medium

**Derived from:**
- `interview_cataloging_2009-05-08.txt`

The system shall provide data quality reports for invalid item types, overly long call numbers, and bibliographic records without item records, and shall show the last item edit date excluding circulation activity. Threshold for “long call number” and the precise distinction between edits and circulation updates are unspecified.

### REQ-089: Cross-platform deployment on Linux and Solaris

**Priority:** High

**Derived from:**
- `interview_sysadmin_2009-05-10.txt`

The reporting system must operate in PINES server environments including Red Hat Enterprise Linux and Solaris 10 on SPARC hardware. The transcript does not define supported versions or required parity between environments.

### REQ-090: Non-disruptive search/report processing during open hours

**Priority:** High

**Derived from:**
- `interview_sysadmin_2009-05-10.txt`
- `meeting_minutes/meeting_2009-07-20_minutes.txt`

Searches and reports must be processed during open hours without disrupting circulation, the OPAC, or other system functions. No measurable performance limits or acceptable disruption definition is provided.

### REQ-091: Legacy browser support (IE 6.0+ and Firefox 2.0+)

**Priority:** Low

**Derived from:**
- `interview_sysadmin_2009-05-10.txt`

The reporting system must support Microsoft Internet Explorer 6.0 and later and Firefox 2.0 and later. The document does not specify supported operating systems, browser feature levels, or testing requirements.

### REQ-092: Section 508 accessibility compliance

**Priority:** High

**Derived from:**
- `interview_sysadmin_2009-05-10.txt`
- `meeting_minutes/meeting_2009-07-20_minutes.txt`
- `early_draft_srs_galecia.txt`

The system must comply with Section 508 accessibility requirements and support screen readers, screen magnification software, and other assistive technologies. The applicable Section 508 version and verification criteria are not specified.

### REQ-093: Accessible HTML output using semantic structure, alt tags, and ARIA labels

**Priority:** High

**Derived from:**
- `interview_sysadmin_2009-05-10.txt`

HTML output must use alt tags, ARIA labels, semantic HTML, and standards-compliant HTML structure. Required HTML standard and detailed accessibility rules are not identified.

### REQ-094: Use relational PostgreSQL structure; support complex relational queries

**Priority:** High

**Derived from:**
- `interview_sysadmin_2009-05-10.txt`
- `meeting_tech_subcommittee_2009-06-30.txt`
- `meeting_minutes/meeting_2009-07-20_minutes.txt`

The reporting system must work with PINES's relational PostgreSQL database structure and support complex relational queries without requiring a separate denormalized reporting schema. The required PostgreSQL version and whether separate read-only structures are prohibited are unclear.

### REQ-095: Administrable role/security-group-based access for multiple staff/patron roles

**Priority:** High

**Derived from:**
- `interview_sysadmin_2009-05-10.txt`

The system must provide administrable role- or security-group-based access control for patrons, staff, local administrators, global administrators, individuals, workgroups, and arbitrary staff groups, with permission changes managed through role assignment. The exact permissions for each role and whether both security groups and roles are required are not fully defined.

### REQ-096: Separate development/training environments and migrate configuration to production

**Priority:** High

**Derived from:**
- `interview_sysadmin_2009-05-10.txt`
- `meeting_minutes/meeting_2009-07-20_minutes.txt`
- `meeting_tech_subcommittee_2009-06-30.txt`

The system must provide separate development and training environments that do not affect production, with export/import capability to migrate report templates, permission settings, and other configuration to production. Migration scope, controls, rollback behavior, and full set of migratable configuration are unspecified.

### REQ-097: Online hierarchical cross-linked searchable help for report use

**Priority:** Medium

**Derived from:**
- `interview_sysadmin_2009-05-10.txt`

The system must provide online help that is hierarchical, cross-linked, searchable, and easy to navigate for staff learning how to run reports. No ownership/content scope/accessibility/maintenance process is specified.

### REQ-098: Reports Working Group filters all new Reports development

**Priority:** Low

**Derived from:**
- `meeting_minutes/meeting_2009-03-15_minutes.txt`

All new Reports development shall be filtered through the Reports Working Group as the Reports testing group. The meaning of “filtered” and the group’s approval authority are unspecified.

### REQ-099: Compile report inventory for an Executive Reports Interface

**Priority:** Low

**Derived from:**
- `meeting_minutes/meeting_2009-03-15_minutes.txt`

The project shall compile a list of reports needed for an Executive Reports Interface. Interface scope and criteria for determining needed reports are unspecified.

### REQ-100: Determine and create PINES report templates for all libraries

**Priority:** Medium

**Derived from:**
- `meeting_minutes/meeting_2009-03-15_minutes.txt`

The project shall determine and create templates needed for all PINES libraries. Required template types, content, and customization rules are unspecified.

### REQ-101: Management analysis and oversight reporting capabilities

**Priority:** Medium

**Derived from:**
- `meeting_minutes/meeting_2009-03-15_minutes.txt`

The reporting capability shall support management-process analysis of library collection use, branch capacity and collection distribution, patron demographics and interests, staff productivity and workflow, and financial transaction tracking and verification. Required analyses/measures/data sources/verification behavior are not defined.

### REQ-102: Reporting scope excludes day-to-day OPAC and circulation client functions

**Priority:** Medium

**Derived from:**
- `meeting_minutes/meeting_2009-03-15_minutes.txt`

The requirements shall address management activities and exclude day-to-day patron-facing functions handled by the OPAC and circulation client. Boundary clarification may be needed.

### REQ-103: Defer detailed UI and data-structure specification to later iteration

**Priority:** Low

**Derived from:**
- `meeting_minutes/meeting_2009-03-15_minutes.txt`

Detailed user-interface and data-structure requirements shall be specified later using an iterative, prototype-oriented methodology; the current effort focuses on functional requirements. Timing/ownership/deliverables are unspecified.

### REQ-104: Conduct staff interviews to gather report needs by April 15, 2009

**Priority:** Low

**Derived from:**
- `meeting_minutes/meeting_2009-03-15_minutes.txt`

Each working-group member shall conduct at least one interview with staff in their library system to gather report needs by April 15, 2009. Interview format and expected output are unspecified.

### REQ-105: Non-functional: consortium scale support with non-disruptive open-hours processing

**Priority:** High

**Derived from:**
- `meeting_minutes/meeting_2009-07-20_minutes.txt`

Management Processes shall support a consortium with 286 locations, 17 million annual circulations, and over 900,000 items purchased and processed annually, while allowing searches and reports to run during open hours without disrupting other system functions. Performance targets and acceptable impact are not quantified.

### REQ-106: Supported server and client platforms (Linux/Solaris; web and Windows client; IE/Firefox)

**Priority:** Medium

**Derived from:**
- `meeting_minutes/meeting_2009-07-20_minutes.txt`

Management Processes shall operate on Linux or Solaris servers and be accessible through a web browser or a Windows-compatible client, with browser access supporting Microsoft Internet Explorer 6.0+ and Mozilla Firefox 2.0+. It is unclear whether both access modes are mandatory and whether functionality equivalence is required across them.

### REQ-107: Accessibility with assistive technology consistent with Section 508

**Priority:** High

**Derived from:**
- `meeting_minutes/meeting_2009-07-20_minutes.txt`

Management Processes shall be accessible with screen-reading, screen-magnification, and other assistive software designed to increase accessibility, including support consistent with Section 508 requirements. The document does not define measurable conformance beyond Section 508 compliance.

### REQ-108: Use fully relational database backend for Management Processes

**Priority:** Medium

**Derived from:**
- `meeting_minutes/meeting_2009-07-20_minutes.txt`

Management Processes shall use a fully relational database back end. No specific relational database technology or compatibility requirements are stated.

### REQ-109: Developer provides data specifications and high-level process descriptions for major processes

**Priority:** Medium

**Derived from:**
- `meeting_minutes/meeting_2009-07-20_minutes.txt`

The software developer shall provide complete data specifications for records maintained or accessed by Management Processes and thorough high-level descriptions of major processes, including bibliographic import/export, authority validation, and standard reports. Documentation format and update frequency are not defined.

### REQ-110: Online hierarchical HTML help plus admin error and query feedback

**Priority:** Medium

**Derived from:**
- `meeting_minutes/meeting_2009-07-20_minutes.txt`

The system shall provide an online, hierarchical, cross-linked HTML help system describing and illustrating all system functions, along with high-level error feedback and query-specific feedback for Local and Global System Administrators through the front-end interface. Maintenance and security controls for low-level diagnostics are not specified.

### REQ-111: Produce W3C standards-compliant HTML for web interface and outputs

**Priority:** Medium

**Derived from:**
- `meeting_tech_subcommittee_2009-06-30.txt`

The web interface, help system, and report output must produce HTML that validates against W3C standards.

### REQ-112: Migrate templates, permission settings, and saved queries between environments

**Priority:** High

**Derived from:**
- `meeting_tech_subcommittee_2009-06-30.txt`

The system must support migration of templates, permission settings, and saved queries between development, training, and production environments; the training environment must protect production data from experimentation. Migration direction/safeguards are unspecified.

### REQ-113: Role-based access control with Global Admin, Local Admin, Library Manager, Staff, and patron indirect access

**Priority:** High

**Derived from:**
- `meeting_tech_subcommittee_2009-06-30.txt`

The system must provide security groups or roles for access control with access levels including Global Admin, Local Admin, Library Manager, Staff, and indirect Patron access. Exact permissions beyond the summaries are not fully specified.

### REQ-114: OPAC isolation: reports must not slow OPAC and must not modify OPAC data

**Priority:** High

**Derived from:**
- `meeting_tech_subcommittee_2009-06-30.txt`

The management reporting system must remain separate from the public catalog, must not slow down the OPAC while reports run, and must query OPAC data without modifying it. No measurable performance threshold is defined.

### REQ-115: Developer provides data specifications and data dictionaries with major process descriptions

**Priority:** Medium

**Derived from:**
- `meeting_tech_subcommittee_2009-06-30.txt`

The developer must provide complete data specifications and data dictionaries for maintained or accessed record types, plus high-level descriptions of major processes and standard reports. The phrase “other records” is not exhaustively enumerated.

### REQ-116: Accessible hierarchical online help in HTML for screen readers

**Priority:** Medium

**Derived from:**
- `meeting_tech_subcommittee_2009-06-30.txt`

The system must provide an online, hierarchical, cross-linked help system in HTML that is accessible to screen readers.

### REQ-117: High-level error reporting with query-specific low-level administrator feedback

**Priority:** Medium

**Derived from:**
- `meeting_tech_subcommittee_2009-06-30.txt`

The system must provide thorough high-level error reporting and feedback, with query-specific low-level feedback available to administrators (e.g., which table/field and what kind of error). Required detail and administrator roles are not defined more precisely.

### REQ-118: Report output formats: Excel, HTML, and CSV

**Priority:** High

**Derived from:**
- `meeting_tech_subcommittee_2009-06-30.txt`

Reports must be available in Excel, HTML, and CSV formats.

### REQ-119: Support real-time and historical reporting (historical warehouse approach tentative)

**Priority:** Medium

**Derived from:**
- `meeting_tech_subcommittee_2009-06-30.txt`

The reporting capability must support both real-time reports and historical reports; the possible use of a reporting warehouse for historical data remains to be determined. Historical retention requirements are unspecified.

### REQ-120: Vendor data integration via APIs and/or standard files with tolerance for missing data

**Priority:** Medium

**Derived from:**
- `meeting_tech_subcommittee_2009-06-30.txt`

The management reporting processes must interface with vendor websites through published APIs and/or standard-format data files, including formats such as USMARC21 and EDIFACT, while tolerating the absence of such data at some libraries. Supported vendors/APIs/file formats and behavior when data is absent are not specified.

### REQ-121: Transaction history retention for configurable X days with indefinite monthly/annual aggregates

**Priority:** Medium

**Derived from:**
- `survey_results_2009.txt`

The system shall retain transaction history for a configurable number of days and retain monthly and annual aggregates indefinitely. The required number of days represented by X is not specified.

### REQ-122: Group transaction reports by hour, terminal, branch, and system

**Priority:** Medium

**Derived from:**
- `survey_results_2009.txt`

Reports shall support grouping transactions by hour, terminal, branch, and system.

### REQ-123: Count check-ins individually and cumulatively by type

**Priority:** Medium

**Derived from:**
- `survey_results_2009.txt`

Reports shall count check-ins individually and cumulatively by check-in type, including book-drop, terminal, and self-service or user-performed check-ins. The category “by user” is unclear and may overlap with other categories.

### REQ-124: Count checkouts and renewals individually and cumulatively by type

**Priority:** Medium

**Derived from:**
- `survey_results_2009.txt`

Reports shall count checkout and renewal types individually and cumulatively, including staff checkout, self checkout, staff renewal, self checkout renewal, online renewal, and OPAC renewal.

### REQ-125: Aggregate holds and transactions including placement method and geographic grouping

**Priority:** Medium

**Derived from:**
- `survey_results_2009.txt`

Transaction reports shall identify hold placement method and show holds placed, holds filled, and check-outs aggregated per patron, library, group of libraries, system, and county.

### REQ-126: Provide anonymized demographic and behavior analysis by region and age range

**Priority:** Medium

**Derived from:**
- `survey_results_2009.txt`

The system shall provide anonymized demographic statistics by geographical region and age range, and produce statistics to understand or predict patron behavior and material use. The required behavior measures/prediction method and validation criteria are not specified.

### REQ-127: Expand available report types to cover identified reporting gaps

**Priority:** Low

**Derived from:**
- `evergreen_reference_2009.txt`

The management processes reporting system should expand available report types to cover report gaps identified for circulation, items, bibliographic records, patrons, bills, holds, and related collection data. The source lists missing or limited reports but does not define a prioritized scope or acceptance criteria.

### REQ-128: Fine-grained control over who can create vs. run reports and template management

**Priority:** Low

**Derived from:**
- `evergreen_reference_2009.txt`

The reporting system should provide fine-grained report permissions and report template management, including separate control over report creation and execution. Required permission roles, sharing model, and template lifecycle are not specified.

### REQ-129: Report queue visibility with prioritizing and cancelling controls

**Priority:** Low

**Derived from:**
- `evergreen_reference_2009.txt`

The reporting system should provide report queue visibility and status indicators, with support for prioritizing and cancelling reports. Queue states, prioritization rules, cancellation behavior, and authorization are undefined.

### REQ-130: Scheduling and delivery options including ASAP/hourly/daily/weekly/monthly/yearly plus email delivery and address book

**Priority:** Low

**Derived from:**
- `evergreen_reference_2009.txt`

The reporting system should provide multiple output formats and expanded scheduling options, including ASAP, hourly, daily, weekly, monthly, and yearly execution, with email delivery and report-delivery address-book support. Supported formats, scheduling semantics, delivery failure handling, and address-book ownership rules are not defined.

### REQ-131: Non-functional: accessibility support for report interface

**Priority:** Low

**Derived from:**
- `evergreen_reference_2009.txt`

The report interface should provide accessibility support or comply with accessibility requirements. No accessibility standard, conformance level, or specific interface requirements are identified.

### REQ-132: Separate reporting from production operations via reporting database/replica and background processing

**Priority:** Low

**Derived from:**
- `evergreen_reference_2009.txt`

Reporting should be separated from production operations through a separate reporting database or replica and background processing for long-running reports. The source does not define data freshness/consistency, performance targets, or which workloads require background processing.

### REQ-133: Provide dev/training environment separation and configuration migration

**Priority:** Low

**Derived from:**
- `evergreen_reference_2009.txt`

The reporting system should provide a development/training environment with the ability to migrate configuration between environments. Environment boundaries, migration scope, migration direction, and safeguards are unspecified.

### REQ-134: Reporting result completeness: real-time, historical warehouse, nulls/blanks, selection criteria display, and file-based filtering (unelaborated)

**Priority:** Low

**Derived from:**
- `evergreen_reference_2009.txt`

Reporting should support identified data and result requirements including real-time and historical reporting, selection-criteria display, required null and blank fields, separate last-circulation information, and report filtering from uploaded text files. Several behaviors are grouped together with undefined details such as retention period, supported fields, and processing rules.

### REQ-135: Users can see report queue position and status

**Priority:** Low

**Derived from:**
- `survey_results_2009.txt`

Users shall be able to see where their report is in the report queue. This is consistent with the separate requirement for queue visibility but specifically emphasizes user visibility.

### REQ-136: Unresolved: define branch capacity metrics before building interface

**Priority:** High

**Derived from:**
- `conversations/conv_pines015_capacity_interface.eml`

Before building the capacity interface, the system must establish which metric or metrics define “branch capacity.” Multiple candidate definitions are mentioned (e.g., item count versus shelf space, configured limits, circulation versus processing capacity), but none are selected in the source.

## Blacklist

### Discarded: Denied deletion attempt tracking

**Reason:** Ambiguous/“helpful” and not stated as a consolidated mandatory requirement in the sources (described as something that would be helpful rather than a firm requirement).

**Sources:**
- `conversations/conv_pines022_deletions.eml`

### Discarded: Report cancellation

**Reason:** Marked unsupported/feasibility note in the source (“technically feasible”) rather than an approved requirement.

**Sources:**
- `meeting_tech_subcommittee_2009-06-30.txt`

### Discarded: Reports development testing gate (filtered through the Reports Working Group as the Reports testing group)

**Reason:** Discarded in the first-pass consolidation to avoid duplicating/over-specifying an already captured governance item; however, it is retained above as a requirement keyed separately under the working group filtering statement.

**Sources:**
- `meeting_minutes/meeting_2009-03-15_minutes.txt`

### Discarded: Some requirements about reporting data and result requirements that bundle multiple undefined behaviors (real-time/historical warehouse, selection criteria display, null/blank behavior, last-circulation separation, and filtering from uploaded text files)

**Reason:** Too broad as an acceptance-scope definition; however, the source capability is still captured above as one low-priority requirement rather than discarded.

**Sources:**
- `evergreen_reference_2009.txt`

## Merged Candidate Trace

- **Merged into `missing-damaged-items-report-grouped-per-branch`:** The missing/damaged report and in-transit report requirements shall be tracked separately in the requirements documentation.
  - Reason: Preserved as distinct requirements for each independent capability; the candidate is about documentation tracking rather than changing the functionality requirements.
  - Source: `conversations/conv_pines019_020_missing_intransit.eml`
- **Merged into `auto-revert-transfers-after-time-and-or-criteria`:** Batch item transfer utility shall support ... reverting items to their original location after a set period of time.
  - Reason: Same semantic capability: revert transferred items back after a specified period; the interview source omits criteria details present elsewhere, but the core capability matches.
  - Source: `interview_cataloging_2009-05-08.txt`
  - Source: `conversations/conv_pines018_item_transfer.eml`
- **Merged into `unified-transit-direction-report`:** Missing, damaged, and in-transit item reports ... combined transit report ... per branch and per system ... merge transit-to and transit-from into one report.
  - Reason: Exact merge on the unified transit-direction behavior; other missing/damaged details are covered by separate requirements.
  - Source: `interview_cataloging_2009-05-08.txt`
  - Source: `conversations/conv_pines019_020_missing_intransit.eml`
- **Merged into `missing-and-damaged-items-report-grouped-by-branch`:** The system shall provide reports of missing and damaged items grouped per branch.
  - Reason: Same actor/workflow/data/outcome as already kept under the dedicated missing/damaged report requirement.
  - Source: `conversations/conv_pines019_020_missing_intransit.eml`
  - Source: `interview_cataloging_2009-05-08.txt`
- **Merged into `consortium-scale-with-open-hours-non-disruption`:** Management Processes shall support ... consortium with 286 locations, 17 million annual circulations, and over 900,000 items ... while allowing searches and reports to run during open hours without disrupting other system functions.
  - Reason: Duplicate semantic requirement with same scale and non-disruption outcome captured in a single requirement.
  - Source: `meeting_minutes/meeting_2009-07-20_minutes.txt`

## Generation Metadata

- Source documents: 20
- Review rounds: 2

## Unresolved Review Issues

- Candidate 'Report cancellation' is present in the candidates but the requirements merged/discarded notes mark this as unsupported — either remove the candidate or supply an authoritative source/approval that it is a required capability.
- Candidate 'Denied deletion attempt tracking' appears in candidates but was explicitly discarded in the requirements summary; either provide a source that elevates it to a requirement or remove it from the candidate set.
- Volume-state semantics are ambiguous: candidate 'Volume by material state' does not define whether 'new acquisitions' is mutually exclusive from 'on-shelf' or 'in-circulation' counts; clarify state definitions, mutual exclusion, and aggregation rules.
- Holds-count semantics are undefined: candidate 'Holds counts' does not specify the counting unit (item-level, transaction, request) or aggregation rules for multiple holds; define the metric and aggregation method.
- Date semantics are missing: candidates 'Historical volume filtering' and 'Acquisition-date reporting' lack precise definitions for date semantics, supported date ranges, and standard reporting periods (e.g., what constitutes a point-in-time versus range, timezone rules, default windows).
- Capacity metric undefined: candidates for capacity (e.g., 'All-branch capacity overview', 'Capacity definition', 'Capacity trend data') do not state which metric(s) constitute 'capacity' (item count, shelf space, configured limits, processing throughput). Define the canonical capacity metric(s) and derivation rules.
- Usability acceptance missing: candidate '286-location overview constraint' requires that the 286-location overview not be unusably crowded but provides no measurable usability threshold or required mitigation (grouping, paging, aggregation); define acceptance criteria and mitigation options.
- Performance/SLA details missing: non-functional candidates such as 'Scale batch processing' and 'Non-disruptive report processing' specify scale and non-disruption but provide no measurable performance targets, concurrency limits, or acceptable impact thresholds; add concrete performance requirements or test criteria.
- Privacy/anonymization underspecified: 'Privacy-preserving transaction archive' and related candidates require anonymization per state law but do not reference applicable laws, anonymization techniques, re-identification controls, or authorized-exception rules; provide legal references and anonymization policy/technique requirements.
- RBAC model underspecified: candidates about roles and fine-grained report permissions ('Role-based access and report permissions', 'Role-based access control', 'Report permissions and roles') do not define the permission model, how multiple roles' precedence is resolved, or administrative processes for role lifecycle; define a canonical permission model and precedence rules.
- Financial reporting ambiguity: candidates 'Financial reporting', 'Data retention enforcement', and 'Balance threshold queries' do not define which financial data are subject to seven-year retention, how payment methods relate to collection channels, nor the exact definition of 'balance' used in thresholds; define retained data sets, reconciliation rules, and balance semantics.
- Query tool and validation gaps: 'Query-and-reporting-tools-across-record-types' and 'Query design tool' candidates lack required schema dictionaries, validation rules (including safe regex usage), limits on complexity, and expected UI behaviors for composing queries; attach schema/dictionary references and validation rules.
- Documentation/versioning obligations missing: 'Developer-provided data and process documentation' and 'Online help' candidates do not specify update frequency, versioning, ownership, or accessibility/version conformance for documentation; specify documentation SLAs and maintenance responsibilities.
- Naming / traceability collisions: identical short candidate names are used for distinct scopes (examples: multiple 'CSV export' entries and multiple 'Report queue visibility' entries). Add scope/context to candidate names (e.g., 'CSV export — capacity', 'CSV export — inactive-patrons') to preserve traceability.
- Merge Report queue visibility into Report queue visibility: Two candidate entries use the exact same name and semantics (staff/users must be able to see their report's queue position/status). These are semantic duplicates and should be merged into a single requirement to avoid duplicate implementation/tracking.
