#!/usr/bin/env python
import os
import shutil
import sys
import subprocess
import json
import yaml
import inflect
from scaffold.custom_fields import *
from scaffold.modules.replace_string import replace_string, \
new_route_string, menu_string, js_src_string, test_script_string, conf_js_string
from scaffold.modules.errors import BlueprintError

blueprint_file = 'app/__init__.py'
test_script = 'tests.bash'
yaml_file = sys.argv[1]
app_js_file = "app/templates/static/js/app.js"
main_index_file = "app/templates/index.html"
conf_js_file = "conf.js"

# Error classes
def make_plural(resource):
    # https://pypi.python.org/pypi/inflect
    p = inflect.engine()
    if p.singular_noun(resource):
        resources = resource
        resource = p.singular_noun(resource)
        return resource, resources
    else:
        resources = p.plural(resource)
        return resource, resources

def generate_files(module_path):

    app_files = ['views.py', 'models.py', '__init__.py', 'tests.py']

    for file in app_files:

        # Generate App files
        if file == "views.py":
            with open(os.path.join(module_path, 'views.py'), "w") as new_file:
                with open("scaffold/app/views.py", "r") as old_file:
                    for line in old_file:
                        new_file.write(line.format(resource=resource,
                                                   resources=resources,
                                                   Resources=resources.title(),
                                                   Resource=resource.title(),
                                                   add_fields=add_fields))

        elif file == "models.py":
            with open(os.path.join(module_path, 'models.py'), "w") as new_file:
                with open("scaffold/app/models.py", "r") as old_file:
                    for line in old_file:
                        new_file.write(line.format(resource=resource, resources=resources,
                                                   Resources=resources.title(),
                                                   db_rows=db_rows,
                                                   schema=schema, meta=meta,
                                                   init_self_vars=init_self_vars,
                                                   init_args=init_args))

        elif file == "__init__.py":
            with open(os.path.join(module_path, '__init__.py'), "w") as new_file:
                with open("scaffold/app/__init__.py", "r") as old_file:
                    for line in old_file:
                        new_file.write(line)

        # Tests
        elif file == "tests.py":
            with open(os.path.join(module_path, 'test_{}.py'.format(resources)), "w") as new_file:
                with open("scaffold/app/tests.py", "r") as old_file:
                    for line in old_file:
                        new_file.write(line.format(resource=resource, resources=resources,
                                                   Resources=resources.title(),
                                                   test_add_fields=json.dumps(
                                                       test_add_fields),
                                                   test_update_fields=json.dumps(
                                                       test_update_fields)))


def register_blueprints():
    string_to_insert_after = '# Blueprints'
    new_blueprint = """
    # Blueprints
    from app.{resources}.views import {resources}
    app.register_blueprint({resources}, url_prefix='/api/v1/{resources}')""".format(resources=resources)
    with open(blueprint_file, 'r+') as old_file:
        filedata = old_file.read()
    if string_to_insert_after in filedata:
        # replace the first occurrence
        new_filedata = filedata.replace(
            string_to_insert_after, new_blueprint, 1)
        with open(blueprint_file, 'w') as new_file:
            new_file.write(new_filedata)
            print("Registered Blueprints for ", resources)
    else:
        raise BlueprintError()


def clean_up(module_path):
    if os.path.isdir(module_path):
        shutil.rmtree(module_path)


def run_autopep8():
    try:
        cmd_output = subprocess.check_output(
            ['autopep8', '--in-place', '--recursive', 'app'])
        print("Ran autopep8")
    except subprocess.CalledProcessError:
        print("autopep8 failed")
        raise

# Main Code Start
#
# Parse YAML file
with open(yaml_file, "r") as file:

    yaml_data = yaml.load(file)

    for module, fields in yaml_data.items():
            # make module name plural
        resource, resources = make_plural(module)

        # Start strings to insert into models
        db_rows = ""
        schema = ""
        meta = ""
        init_self_vars = ""
        init_args = ""
        # End strings to insert into models

        # Start strings to insert into views
        add_fields = ""

        # strings to insert into _form.html
        form_args = []
        form_fields = ""

        # strings to insert into update.html
        update_form_args = ""

        # strings to insert into index.html
        field_table_headers = ""
        index_fields = ""

        # strings to insert into tests.py
        test_add_fields = {}
        test_update_fields = {}

        # Fields to insert into controller.js
        controller_fields = ""
        radio_button_default =""

        # Fields to add to protractor spec.js
        protractor_page_objects = ""
        protractor_edit_elments = ""
        protractor_add_elments = ""

        for f in fields:
            field, field_type = f.split(':')
            if field_type == "string":
                db_rows += """
    {} = db.Column(db.String(250), nullable=False)""".format(field)
                schema += """
    {} = fields.String(validate=not_blank)""".format(field)
                test_add_fields[field] = string_test
                test_update_fields[field] = update_string_test

            elif field_type == "boolean":
                db_rows += """
    {} = db.Column(db.Boolean, nullable=False)""".format(field)
                schema += """
    {} = fields.Boolean(required=True)""".format(field)
                test_add_fields[field] = boolean_test
                test_update_fields[field] = update_boolean_test

            elif field_type == "integer":
                db_rows += """
    {} = db.Column(db.Integer, nullable=False)""".format(field)
                schema += """
    {} = fields.Integer(required=True)""".format(field)
                test_add_fields[field] = integer_test
                test_update_fields[field] = update_integer_test


            elif field_type == "biginteger":
                db_rows += """
    {} = db.Column(db.BigInteger, nullable=False)""".format(field)
                schema += """
    {} = fields.Integer(required=True)""".format(field)
                test_add_fields[field] = big_integer_test
                test_update_fields[field] = update_big_integer_test

            elif field_type == "email":
                db_rows += """
    {} = db.Column(db.String(250), nullable=False)""".format(field)
                schema += """
    {} = fields.Email(validate=not_blank)""".format(field)
                test_add_fields[field] = email_test
                test_update_fields[field] = update_email_test


            elif field_type == "url":
                db_rows += """
    {} = db.Column(db.String(250), nullable=False)""".format(field)
                schema += """
    {} = fields.URL(validate=not_blank)""".format(field)
                test_add_fields[field] = url_test
                test_update_fields[field] = update_url_test


            elif field_type == "datetime":
                db_rows += """
    {} = db.Column(db.TIMESTAMP,server_default=db.func.current_timestamp(),nullable=False)""".format(field)
                schema += """
    {} = fields.DateTime(required=True)""".format(field)
                test_add_fields[field] = date_time_test
                test_update_fields[field] = update_date_time_test


            elif field_type == "date":
                db_rows += """
    {} = db.Column(db.Date, nullable=False)""".format(field)
                schema += """
    {} = fields.Date(required=True)""".format(field)
                test_add_fields[field] = date_test
                test_update_fields[field] = update_date_test

            elif field_type == "decimal":
                db_rows += """
    {} = db.Column(db.Numeric, nullable=False)""".format(field)
                schema += """
    {} = fields.Decimal(as_string=True)""".format(field)
                test_add_fields[field] = decimal_test
                test_update_fields[field] = update_decimal_test

            elif field_type == "text":
                db_rows += """
    {} = db.Column(db.Text, nullable=False)""".format(field)
                schema += """
    {} = fields.String(validate=not_blank)""".format(field)
                test_add_fields[field] = text_test
                test_update_fields[field] = update_text_test

            # models
            meta += """ '{}', """.format(field)
            init_args += """ {}, """.format(field)
            init_self_vars += """
        self.{field} = {field}""".format(field=field)
            # Views
            add_fields += add_string.format(field)

            #_form.html
            form_args.append(
                """{resource}_{field} = ''""".format(resource=resource, field=field))
            field_table_headers += """ <th>{field}</th> """.format(field=field)
            index_fields += """<td>{{{{ result['{field}'] }}}}</td>""".format(
                field=field)
            update_form_args += """{resource}_{field} = {resource}.{field}, """.format(resource=resource, field=field)

            # controller.js
            controller_fields += controller_field.format(field=field)


        # Generate files with the new fields
        module_dir = os.path.join('app', resources)

        try:
            os.mkdir(module_dir)

            try:
                generate_files(module_dir)
                print('{} created successfully'.format(module_dir))
                register_blueprints()

                # Add tests to test.bash
                replace_string(
                    resource, resources, test_script, "#TESTS", test_script_string)

                run_autopep8()
            except:
                clean_up(module_dir)
                raise

        except:
            raise
