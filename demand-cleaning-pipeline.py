# ==================================================
# STEP 1 — IMPORT LIBRARIES
# ==================================================

import pandas as pd


# ==================================================
# STEP 2 — DEFINE FILE PATH
# ==================================================

path = r"C:\Users\chino\OneDrive\Escritorio\python practices"

# ==================================================
# STEP 3 — LOAD DEMAND FILE
# ==================================================

df = pd.read_csv(
    path + r"\1. ZF263 2025-12-15 Demanda.csv",
    encoding="latin1"
)


# ==================================================
# STEP 4 — INITIAL DATA INSPECTION
# ==================================================

print(df.head(20))

print(df.columns.to_list())

print(df.shape)

print(df.info())


# ==================================================
# STEP 5 — FORWARD FILL FG VALUES
# ==================================================

df["USIP/N"] = df["USIP/N"].ffill()

df["USIP/NDescription"] = df["USIP/NDescription"].ffill()

print(df.head(20))


# ==================================================
# STEP 6 — FILTER PROJECT FG
# ==================================================

fg_list = [
    "6971-0009-05",
    "6971-0010-05",
    "6971-0011-02",
    "6971-0012-02",
    "6971-0013-02",
    "6971-0014-02",
    "6971-0015-02",
    "6971-0016-02",
    "6971-0017-02",
    "6971-0018-02",
    "6971-0019-02",
    "6971-0020-02"
]

project_df = df[df["USIP/N"].isin(fg_list)]

print(project_df.shape)

print(project_df["USIP/N"].unique())

# ==================================================
# STEP 7 — IDENTIFY FIRST 12 DEMAND WEEKS
# ==================================================

week_columns = [
    col for col in project_df.columns
    if col.startswith("WK.")
    and col.count(".") == 1
]

week_columns = week_columns[:12]

print(week_columns)

# ==================================================
# STEP 8 — CONSOLIDATE TO 1 ROW PER FG
# ==================================================

for col in week_columns:
    project_df[col] = pd.to_numeric(
        project_df[col],
        errors="coerce"
    ).fillna(0)

print(project_df[week_columns].dtypes)

columns_to_sum = [
    "STOCK",
    "Supply",
    "Demand",
    "Cum. Delta",
    "Overdue"   
] + week_columns

clean_df = (
    project_df
    .groupby(
        ["USIP/N", "USIP/NDescription"],
        as_index=False
    )[columns_to_sum]
    .sum()
    )

print(clean_df.head())

print(clean_df.shape)

# ==================================================
#  STEP 9 — RENAME COLUMNS
# ==================================================

clean_df = clean_df.rename(columns={
    "USIP/N": "FG",
    "USIP/NDescription": "FG Description",
    "Supply": "WIP",
    "Cum. Delta": "Backlog"
})

print(clean_df.columns.to_list())


# ==================================================
# STEP 10 — REORDER COLUMNS
# ==================================================

final_columns = [
    "FG",
    "FG Description",
    "STOCK",
    "WIP",
    "Demand",
    "Backlog",
    "Overdue"
] + week_columns

clean_df = clean_df[final_columns]

print(clean_df.head())

# ==================================================
# STEP 11 — EXPORT CLEAN FILE
# ==================================================

clean_df.to_csv(
    path + r"\clean_demand.csv",
    index=False
)

print("Demand cleaning completed successfully.")