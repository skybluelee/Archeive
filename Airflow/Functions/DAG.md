# DAG
해당 문서는 [airflow.models.dag](https://airflow.apache.org/docs/apache-airflow/stable/_api/airflow/models/dag/index.html#module-contents)의 일부를 해석한 내용이다.

# airflow.models.dag.DAG
> `classairflow.models.dag.DAG(dag_id, description=None, schedule=NOTSET, schedule_interval=NOTSET, timetable=None, start_date=None, end_date=None, full_filepath=None, template_searchpath=None, template_undefined=jinja2.StrictUndefined, user_defined_macros=None, user_defined_filters=None, default_args=None, concurrency=None, max_active_tasks=airflow_conf.getint('core', 'max_active_tasks_per_dag'), max_active_runs=airflow_conf.getint('core', 'max_active_runs_per_dag'), dagrun_timeout=None, sla_miss_callback=None, default_view=airflow_conf.get_mandatory_value('webserver', 'dag_default_view').lower(), orientation=airflow_conf.get_mandatory_value('webserver', 'dag_orientation'), catchup=airflow_conf.getboolean('scheduler', 'catchup_by_default'), on_success_callback=None, on_failure_callback=None, doc_md=None, params=None, access_control=None, is_paused_upon_creation=None, jinja_environment_kwargs=None, render_template_as_native_obj=False, tags=None, owner_links=None, auto_register=True, fail_stop=False) [source](https://airflow.apache.org/docs/apache-airflow/stable/_modules/airflow/models/dag.html#DAG)`

gg
