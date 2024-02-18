from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,validators,BooleanField,IntegerField,SelectField,DateField,HiddenField
from wtforms.validators import DataRequired,Length,Email,EqualTo
from flask_login import current_user

class RegistrationForm(FlaskForm):
    username=StringField("Username",validators=[DataRequired(),Length(min=2,max=25)])
    email=StringField("Email",validators=[DataRequired(),Email()])
    password=PasswordField("Password",validators=[DataRequired()])
    confirm_password=PasswordField("Confirm Password",validators=[DataRequired(),EqualTo('password')])
    submit=SubmitField("Sign Up")

class LoginForm(FlaskForm):
    username=StringField("Username",validators=[DataRequired()])
    password=PasswordField("Password",validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit=SubmitField("Log In")


class CategoryForm(FlaskForm):
    category = StringField("Category",validators=[DataRequired()])
    submit=SubmitField("Add")

class ProductForm(FlaskForm):
    product =StringField("Product",validators=[DataRequired()])
    price = IntegerField("Price",validators=[DataRequired()])
    catgory=SelectField("Category",validators=[DataRequired()],default=None)
    stock = IntegerField("Stock",validators=[DataRequired()])
    expiry=DateField("Use By",format='%Y-%m-%d',validators=[DataRequired()])
    submit=SubmitField("Add")

class UpdateCategoryForm(FlaskForm):
    category = StringField("Category",validators=[DataRequired()])
    submit=SubmitField("Update")

class UpdateProductForm(FlaskForm):
    product =StringField("Product",validators=[DataRequired()])
    price = IntegerField("Price",validators=[DataRequired()])
    stock = IntegerField("Stock",validators=[DataRequired()])
    expiry=DateField("Use By",format='%Y-%m-%d',validators=[DataRequired()])
    submit=SubmitField("Update")

class AddToCart(FlaskForm):
    quantity = IntegerField('Quantity')
    id = HiddenField('ID')

class SearchForm(FlaskForm):
    searched=StringField("Searched",validators=[DataRequired()])
    submit=SubmitField("Submit")



