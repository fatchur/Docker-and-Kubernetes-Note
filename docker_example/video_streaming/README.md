### NOTE
- Run socket: `gunicorn -k gevent -w 1 -b 0.0.0.0:8005 main:app`
- Create mysql table: `CREATE TABLE apd_new ( id varchar(100) not null, helm_violation varchar(20), jacket_violation varchar(20), time DATETIME );`
- Set user pwd: `ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'new password';`
