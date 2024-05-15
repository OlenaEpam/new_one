import pytest
from sqlalchemy import create_engine, text
import data_for_tests
from credentails import USERNAME, PASSWORD


@pytest.fixture(scope="session")
def db_connection():
    engine = create_engine(
        f"mssql+pyodbc://{USERNAME}:{PASSWORD}@127.0.0.1/"
        f"TRN?driver=ODBC+Driver+18+for+SQL+Server&charset=utf&autocommit=true&TrustServerCertificate=yes"
    )
    with engine.connect() as connection:
        yield connection


def test_max_salary(db_connection):
    result = db_connection.execute(text("SELECT MAX(max_salary) FROM hr.jobs")).scalar()
    assert result == data_for_tests.MAX_SALARY


def test_avg_salary_in_minimum_range(db_connection):
    result = db_connection.execute(text("SELECT AVG(min_salary) FROM hr.jobs")).scalar()
    assert result == data_for_tests.AVG_SALARY_FOR_MINIMUM_RANGE


def test_count_departments(db_connection):
    result = db_connection.execute(text("SELECT COUNT(department_id) FROM hr.departments")).scalar()
    assert result == data_for_tests.NUMBER_OF_DEPARTMENTS


def test_location_id_in_departments(db_connection):
    expected_list = db_connection.execute(text("SELECT location_id FROM hr.locations")).fetchall()
    actual_list = db_connection.execute(text("Select location_id  from hr.departments")).fetchall()
    assert all(i in expected_list for i in actual_list)


def test_job_id_range(db_connection):
    job_count = db_connection.execute(text("SELECT COUNT(job_id) FROM hr.jobs")).scalar()
    expected_range = list(range(1, job_count+1))
    actual_list_of_job_id_tuples = db_connection.execute(text("SELECT job_id FROM hr.employees")).fetchall()
    actual_list_of_job_id = [i[0] for i in actual_list_of_job_id_tuples]
    for i in actual_list_of_job_id:
        assert i in expected_range, f'{i} not found in expected list'


def test_unique_employee_id(db_connection):
    result = db_connection.execute(text("SELECT employee_id, COUNT(*) FROM hr.employees "
                                        "GROUP BY employee_id HAVING COUNT(*) > 1")).fetchall()
    assert result == []


def test_no_nulls_in_last_name(db_connection):
    result = db_connection.execute(text("SELECT COUNT(*) FROM hr.employees WHERE last_name IS NULL")).scalar()
    assert result == 0