from wtforms import Form, TextAreaField, BooleanField, StringField, PasswordField, SelectField, DecimalField, IntegerField, FileField, validators

class RegistrationForm(Form):
	username = StringField('', [validators.Length(min=4, max=25)], 
		render_kw={'placeholder': 'Username', 'autofocus': True})
	password = PasswordField('', [
		validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')],
        render_kw={'placeholder': 'Password'}
	)
	confirm = PasswordField('',
		render_kw={'placeholder': 'Repeat Password'}
	)


class LoginForm(Form): # Create Login Form
	username = StringField('', [validators.length(min=1)],
		render_kw={'placeholder': 'Username', 'autofocus': True} 
	)
	password = PasswordField('', [
		validators.DataRequired()],
		render_kw={'placeholder': 'Password'}
	)


class OrderForm(Form):  # Create Order Form
    name = StringField('', [validators.length(min=1), validators.DataRequired()],
                       render_kw={'autofocus': True, 'placeholder': 'Full Name'})
    mobile_num = StringField('', [validators.length(min=1), validators.DataRequired()],
                             render_kw={'autofocus': True, 'placeholder': 'Mobile Number'})
    quantity = SelectField('', [validators.DataRequired()],
                           choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')])
    order_place = StringField('', [validators.length(min=1), validators.DataRequired()],
                              render_kw={'placeholder': 'Delivery Address'})


class AddProduct(Form):
	pname = StringField('', [validators.DataRequired()],
						render_kw={'autofocus': True})
	price = DecimalField('', [validators.DataRequired()])
	description = TextAreaField('')
	available = IntegerField('', [validators.DataRequired(), validators.NumberRange(min=1, max=50)])
	category = SelectField('', [validators.DataRequired()],
							choices=[	('tops','Tops'),
										('dress','Dresses'),
										('handbags','Handbags'),
										('shoes','Shoes'),
										('sweaters','Sweaters'),],)

	# cb_tshirt_vshape = BooleanField('V-Shape')
	# cb_tshirt_polo = BooleanField('Polo')
	# cb_tshirt_clean_text = BooleanField('Clean Text')
	# cb_tshirt_design = BooleanField('Colorful Design')

	# cb_wallet_chain = BooleanField('Chain')
	# cb_wallet_leather = BooleanField('Leather')
	# cb_wallet_design = BooleanField('Design')

	# cb_belt_leather = BooleanField('Leather')
	# cb_belt_hook = BooleanField('Hook')
	# cb_belt_color = BooleanField('Color')
	# cb_belt_design = BooleanField('Design')

	# cb_shoes_formal = BooleanField('Formal')
	# cb_shoes_converse = BooleanField('Converse')
	# cb_shoes_loafer = BooleanField('Loafer')
	# cb_shoes_leather = BooleanField('Leather')

	# item = StringField('', render_kw={'placeholder': 'Ex: watch/shoes'})
	pcode = IntegerField('', [validators.DataRequired()])

	# image = FileField('', [validators.DataRequired()])

	# def validate_image(form, field):
	#         if field.data:
	#             field.data = re.sub(r'[^a-z0-9_.-]', '_', field.data)