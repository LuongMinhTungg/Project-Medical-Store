
from manager.model.model import ManagerUser, Role
from flask import Flask, jsonify, request, Response, make_response, render_template, session, Blueprint, flash, redirect, url_for
import jwt
from manager.manager_user.validate import Validate as V
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, DateField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, NumberRange
from wtforms_components import TimeField, read_only
from manager.manager_user.backend import BackEndManagerUser as BU
V = V()
BU = BU()

class ManagementUser:
    def register(self):
        register_form = RegistrationForm(request.form)
        if request.method == 'POST':
            if register_form.validate_on_submit():
                if BU.register() == ('add', 201):
                    return render_template('login.html')
                return render_template('register.html', title='register', form=register_form)
        return render_template('register.html', title='register', form=register_form)

    def login(self):
        form = LoginForm(request.form)
        if request.method == 'POST':
            if form.validate_on_submit():
                try:
                    token = BU.login()
                    resp = redirect(url_for('indexs.index'))
                    resp.set_cookie('token', value=token)
                    return resp
                except TypeError:
                    return render_template('login.html', title='login', form=form)
            else:
                flash('fail')
                return render_template('login.html', title='login', form=form)
        return render_template('login.html', title='login', form=form)

    def insert_user(self,current_user):
        try:
            role = []
            insert_form = InsertUserForm(request.form)
            if current_user.role.name == 'admin':
                insert_form.role.choices = [i.name for i in Role.query.all()]
            if current_user.role.name == 'manager':
                for i in Role.query.all():
                    if i.name != 'admin':
                        role.append(i.name)
                insert_form.role.choices = role
            if request.method == 'POST':
                if insert_form.validate_on_submit():
                    if BU.insert_user(current_user) == ('add', 201):
                        return redirect(url_for('managers.get_all_user'))
                    return redirect(url_for('managers.insert_user'))
            return render_template('register.html', title='insert user', form=insert_form,
                                       current_user=current_user)
        except AttributeError:
            return redirect(url_for('managers.login'))


    def del_user(self,current_user, username):
        try:
            user = ManagerUser.query.filter_by(username=username).first()
            if user:
                if request.method == 'GET':
                    if current_user.role.name == 'manager' and user.role.name == 'admin':
                        return render_template('error_not_role.html', current_user=current_user)
                    BU.del_user(current_user,username)
                    return redirect(url_for('managers.get_all_user'))
                else:
                    return redirect(url_for('managers.get_all_user'))
            else:
                return "Not found user"
        except AttributeError:
            return redirect(url_for('managers.login'))


    def update_user(self,current_user,username):
        try:
            user = ManagerUser.query.filter_by(username=username).first()
            if user:
                if current_user.role.name == 'manager' and user.role.name == 'admin':
                    return render_template('error_not_role.html', current_user=current_user)
                else:
                    if request.method == 'POST':
                        if BU.update_user(current_user,username) == ('update', 202):
                            return redirect(url_for('managers.get_all_user'))
                        return redirect(url_for('managers.get_user', username=username))
                    else:
                        return redirect(url_for('managers.get_user', username=username))
            return render_template('error_not_found.html', current_user=current_user)
        except AttributeError:
            return redirect(url_for('managers.login'))

    def get_all_user(self,current_user):
        try:
            all_user = BU.get_all_user()
            search_form = SearchForm(request.form)
            output_1 = []
            headers = ('name', 'username', 'role', 'phone', 'join_date')
            if request.method == 'GET':
                item = []
                for i in all_user.values():
                    item = [i['name'],i['username'],i['role'],i['phone'],i['join_date']]
                    output_1.append(item)
                return render_template('list_user.html',title='All User', headers=headers, data=output_1,
                                       form=search_form, current_user=current_user, row=item)
            else:
                output_2 = []
                item = []
                list = BU.search_user_by_username()
                for i in list.values():
                    item = [i['name'], i['username'], i['role'], i['phone'], i['join_date']]
                    output_2.append(item)
                return render_template('list_user.html', title='User', headers=headers, data=output_2,
                                       form=search_form,current_user=current_user)

        except AttributeError:
            return redirect(url_for('managers.login'))


    def get_user(self,current_user,username):
        try:
            user_form = UserForm(request.form)
            user = BU.get_user(current_user, username)
            user_form.username.data = user['username']
            user_form.join_date.data = user['join_date']
            if user == ('not role', 404):
                return render_template('error_not_role.html', current_user=current_user)
            else:
                if current_user.role.name == 'admin':
                    user_form.role.choices = [i.name for i in Role.query.all()]
                elif current_user.role.name == 'manager' and user['role'] == 'admin':
                    user_form.role.choices = ['admin']
                elif current_user.role.name == 'manager':
                    user_form.role.choices = ['manager', 'staff']
                elif current_user.role.name == 'staff':
                    user_form.role.choices = ['staff']
                if request.method == 'GET':
                    user_form.name.data = user['name']
                    user_form.phone.data = user['phone']
                    user_form.role.data = user['role']
                    return render_template('user_account.html', title = 'account', form = user_form,current_user=current_user)
                else:
                    if user_form.validate_on_submit():
                        return self.update_user(current_user,username)
                    return render_template('user_account.html', title='account', form=user_form,
                                           current_user=current_user)

        except AttributeError:
            return redirect(url_for('managers.login'))



    def logout(self):
        resp = redirect(url_for('indexs.index'))
        resp.set_cookie('token', value='')
        return resp

    def reset_password(self, current_user,username):
        try:
            reset_password_form = ResetPasswordForm(request.form)
            if request.method == 'POST':
                if BU.reset_password(username) == ('reset', 202):
                    return redirect(url_for('indexs.index'))
                return render_template('reset_password.html', title='reset_password', form=reset_password_form,
                                       current_user=current_user)
            return render_template('reset_password.html',title = 'reset_password', form=reset_password_form,
                                   current_user=current_user)
        except AttributeError:
            return redirect(url_for('managers.login'))

    def change_password(self):
        change_password_form = ChangePasswordForm(request.form)
        if request.method == 'POST':
            if BU.change_password() == ('reset',202):
                return redirect(url_for('indexs.index'))
            return render_template('change_password.html', title='change_password', form=change_password_form)
        return render_template('change_password.html', title='change_password', form=change_password_form)

    def get_all_role(self,current_user):
        all_role = BU.get_all_role()
        output_1 = []
        headers = ('id', 'name')
        item = []
        if request.method == 'GET':
            if all_role:
                for i in all_role.values():
                    item = [i['id'],i['name']]
                    output_1.append(item)
                return render_template('role.html',title='All Role', headers=headers, data=output_1,
                                        current_user=current_user, row=item)
            return render_template('error_not_found.html', current_user=current_user)
        return render_template('role.html', title='All Role', headers=headers, data=output_1,
                               current_user=current_user, row=item)


    def insert_role(self, current_user):
        insert_form = InsertRoleForm()
        if request.method == 'POST':
            if insert_form.validate_on_submit():
                if BU.insert_role() == ('add', 201):
                    return redirect(url_for('managers.get_all_role'))
                return render_template('insert_role.html', title='Insert Role', current_user=current_user, form=insert_form)
        return render_template('insert_role.html', title='Insert Role', current_user=current_user, form=insert_form)

    def update_role(self, current_user, role_id):
        insert_form = InsertRoleForm()
        role = Role.query.filter_by(id=role_id)
        name = ''
        if role:
            for i in role:
                name = i.name
        insert_form.name.data = name
        if request.method == 'GET':
            if role_id == '1':
                flash('cant update admin')
                return redirect(url_for('managers.get_all_role'))
            return render_template('insert_role.html', title='Update Role', current_user=current_user, form=insert_form)
        else:
            BU.update_role(role_id)
            return redirect(url_for('managers.get_all_role'))

    def delete_role(self, current_user, role_id):
        role = Role.query.filter_by(id=role_id)
        if role:
            if request.method == 'GET':
                BU.delete_role(role_id)
                return redirect(url_for('managers.get_all_role'))
            else:
                return redirect(url_for('managers.get_all_role'))
        return render_template('error_not_found.html', current_user=current_user)


class RegistrationForm(FlaskForm):
    name = StringField('Name',validators=[DataRequired(), Length(min=1, max=45)])
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=1, max=45)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Role',validators=[DataRequired()], choices=[i.name for i in Role.query.all()])
    phone = StringField('Phone', validators=[DataRequired(),Length(min=11,max=11)])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = ManagerUser.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),Length(min=1, max=45)])
    password = PasswordField('Password', validators=[DataRequired(),Length(min=1, max=45)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

    def validate_user(self,username):
        user = ManagerUser.query.filter_by(username=username.data).first()
        if not user:
            raise ValidationError('Wrong password or username')



class UserForm(FlaskForm):
    name = StringField('name',validators=[DataRequired(),Length(min=1, max=45)])
    username = StringField('username')
    role = SelectField('role',validators=[DataRequired()],choices=[])
    phone = StringField('phone',validators=[DataRequired(),Length(min=11, max=11)])
    join_date = DateField('join date')
    submit = SubmitField('Change',validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        read_only(self.username)
        read_only(self.join_date)



class ResetPasswordForm(FlaskForm):
    old_password = PasswordField('old_password',validators=[DataRequired()])
    new_password = PasswordField('new_password',validators=[DataRequired()])
    confirm_password = PasswordField('confirm_password',validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Change')

class ChangePasswordForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Length(min=1, max=45)])
    old_password = PasswordField('old_password',validators=[DataRequired()])
    new_password = PasswordField('new_password',validators=[DataRequired()])
    confirm_password = PasswordField('confirm_password',validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Change')

class SearchForm(FlaskForm):
    search = StringField('search')
    submit = SubmitField('Search')

class InsertUserForm(FlaskForm):
    name = StringField('Name',validators=[DataRequired(), Length(min=1, max=45)])
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=1, max=45)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Role',validators=[DataRequired()], choices=[])
    phone = StringField('Phone', validators=[DataRequired(),Length(min=11,max=11)])
    submit = SubmitField('Add')

    def validate_username(self, username):
        user = ManagerUser.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')


class InsertRoleForm(FlaskForm):
    name = StringField('Name',validators=[DataRequired(), Length(min=1, max=45)])
    submit = SubmitField('Add')
    def validate_name(self, name):
        role = Role.query.filter_by(name=name.data).first()
        if role:
            raise ValidationError('That name is taken. Please choose a different one.')
