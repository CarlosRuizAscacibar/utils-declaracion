import os
import sqlite3
import tempfile
import unittest
import pandas as pd

from servicios.validate_dataframe_to_load import remove_present_ids_in_database_with_path, validate_data_frame_to_load
class TestValidateDataframe(unittest.TestCase):
    def test_validate_dataframe_no_duplicates(self):
        df = pd.DataFrame({
            "id": [1, 2, 3],
            "name": ["a", "b", "c"],
        })

        # Should not raise
        validate_data_frame_to_load(df)

    def test_validate_dataframe_with_duplicate_ids(self):
        df = pd.DataFrame({
            "id": [1, 1, 2],
            "name": ["a", "a2", "b"],
        })

        with self.assertRaises(RuntimeError) as ctx:
            validate_data_frame_to_load(df)

        self.assertIn("repeated rows", str(ctx.exception))
    
    def test_single_row(self):
        df = pd.DataFrame({
            "id": [1],
            "name": ["only"],
        })

        validate_data_frame_to_load(df)

    def test_empty_dataframe(self):
        df = pd.DataFrame(columns=["id", "name"])

        validate_data_frame_to_load(df)

    def test_missing_id_column(self):
        df = pd.DataFrame({
            "name": ["a", "b"],
        })

        # SQLite will raise an error
        with self.assertRaises(Exception):
            validate_data_frame_to_load(df)



class TestRemovePresentIdsInDatabase(unittest.TestCase):

    def test_remove_present_ids(self):
        # --- create temporary SQLite database ---
        fd, db_path = tempfile.mkstemp(suffix=".db")
        os.close(fd)

        try:
            conn = sqlite3.connect(db_path)
            conn.execute("""
                create table test_table (
                    id integer primary key
                )
            """)
            conn.executemany(
                "insert into test_table (id) values (?)",
                [(1,), (3,)]
            )
            conn.commit()
            conn.close()

            # --- dataframe with mixed IDs ---
            df_new_rows = pd.DataFrame({
                "id": [1, 2, 3, 4],
                "value": ["a", "b", "c", "d"],
            })

            # --- call function ---
            result = remove_present_ids_in_database_with_path(
                df_new_rows=df_new_rows,
                table="test_table",
                db_path=db_path,
            )

            # --- assertions ---
            self.assertListEqual(
                sorted(result.index.tolist()),
                [2, 4]
            )

            self.assertEqual(
                result.loc[2, "value"],
                "b"
            )

        finally:
            os.remove(db_path)

    def test_no_ids_present_in_database(self):
        # --- create temporary SQLite database ---
        fd, db_path = tempfile.mkstemp(suffix=".db")
        os.close(fd)

        try:
            conn = sqlite3.connect(db_path)
            conn.execute("""
                create table test_table (
                    id integer primary key
                )
            """)
            # NOTE: no rows inserted
            conn.commit()
            conn.close()

            df_new_rows = pd.DataFrame({
                "id": [10, 20, 30],
                "value": ["x", "y", "z"],
            })

            result = remove_present_ids_in_database_with_path(
                df_new_rows=df_new_rows,
                table="test_table",
                db_path=db_path,
            )

            # --- assertions ---
            self.assertListEqual(
                sorted(result.index.tolist()),
                [10, 20, 30]
            )

            self.assertEqual(len(result), 3)

        finally:
            os.remove(db_path)


    if __name__ == "__main__":
        unittest.main()
