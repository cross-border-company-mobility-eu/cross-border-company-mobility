### SQL Files Naming Conventions

This repository contains the SQL scripts categorized by their purpose and functionality in the CbCMdb

- **[DEPRECATED]**: Files prefixed with `[DEPRECATED]` indicate older scripts that are no longer in use but retained for reference purposes. These scripts should not be used for current workflows.
- **control_**: Scripts prefixed with `control_` are designed for validation and data integrity checks. These files include scripts for checking duplicates, matching records with input data, null date checks, and verifying transaction types by year.
- **dev_**: Files with the `dev_` prefix are development scripts that include experimental queries or views under development. These scripts are used for creating new views or modifying existing ones.
- **export_**: Scripts with the `export_` prefix are used for exporting data. These files include queries to retrieve company data or generate time series transaction data for further analysis or reporting.
- **view_**: The `view_` prefix indicates scripts that define database views. These include views for acquiring companies, company thresholds, cross-border transactions, employee thresholds, and merging companies.