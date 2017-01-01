# nb-remote-wordpress-phpunit
Simple python script that enables NetBeans to run phpunit tests on a remote host inside wordpress environment.

## Requirements

1. Install PHPUnit
2. Install WP-CLI

## Prepare wordpress sandox for running phpunit tests

1. Navigate to your remote WordPress install’s main directory:
```Shell
cd /var/www/user12345/htdocs/wp
```
2. Instruct WP-CLI to create the initial unit test files for our plugin called "user12345-plugin":
```Shell
wp scaffold plugin-tests user12345-plugin
```
This will generate all of the files needed for running our phpunit tests.

3. Make sure that phpunit.xml.dist file looks like this:

```
<phpunit
	bootstrap="tests/bootstrap.php"
	backupGlobals="false"
	colors="true"
	convertErrorsToExceptions="true"
	convertNoticesToExceptions="true"
	convertWarningsToExceptions="true"
	>
	<testsuites>
		<testsuite>
			<directory>./tests/</directory>
		</testsuite>
	</testsuites>
        <filter>
            <whitelist>
                <directory suffix=".php">./includes</directory>
                <exclude>
                    <directory suffix=".php">./tests</directory>
                </exclude>
            </whitelist>
        </filter>
</phpunit>
```

4. Run script that creates wordpress installation (sandbox) for running tests:
```Shell
bash bin/install-wp-tests.sh wordpress_test root 12345678 localhost latest
```
Pay attention that this script accepts database name (wordpress_test), database user (root), database password (12345678),
database host (localhost) and wordpress version (latest).
By default this command will create next two folders: "/tmp/wordpress" and "/tmp/wordpress-tests-lib".
The first one contains wordpress installation of "latest" version and the second one contains some
auxiliary classes for runnning phpunit tests inside wordpress environment.

5. I prefer to create permanent wordpress installation for running phpunit tests without need to run install-wp-tests.sh script
every time. Let's do it:

```Shell
mv /tmp/wordpress /var/www/user12345/htdocs/sandbox
mv /tmp/wordpress-tests-lib/* /var/www/user12345/htdocs/sandbox
cd /var/www/user12345/htdocs/sandbox
sed -i "s:'/tmp/wordpress/':dirname(__FILE__) . '/':" wp-tests-config.php
ln -s /var/www/user12345/htdocs/wp/wp-content/plugins/user-switching /var/www/user12345/htdocs/sandbox/wp-content/plugins/
```

6. Check that tests run:
```Shell
cd /var/www/user12345/htdocs/wp/wp-content/plugins/user12345-plugin
WP_TESTS_DIR=/var/www/anton/htdocs/sandbox phpunit
```

## Netbeans configuration

1. Copy nb-remote-wordpress-phpunit.py script to some directory on host machine
2. Replace default configuration inside python script with your preferences
3. Project Properties -> Testing -> PHPUnit -> Use Custom PHPUnit Script
