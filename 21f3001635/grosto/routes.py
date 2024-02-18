from flask import render_template,flash,redirect,url_for,request,session
from grosto import app,db,bcrypt
from grosto.forms import RegistrationForm,LoginForm,CategoryForm,ProductForm,UpdateCategoryForm,UpdateProductForm,AddToCart,SearchForm
from grosto.models import User,Category,Product
from flask_login import login_user, login_required, logout_user,current_user

@app.route("/")
@app.route("/home")
@login_required
def home():
    categories = Category.query.all()
    products=Product.query.all()
    form=AddToCart()
    return render_template("home.html",title="Home",categories=categories,products=products,form=form)

@app.context_processor
def base():
    form_s=SearchForm()
    return dict(form_s=form_s)

@app.route("/register",methods=["GET","POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form=RegistrationForm()
    if form.validate_on_submit():
        hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user=User(username=form.username.data,email=form.email.data,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for user {form.username.data}!','success')
        return redirect(url_for("login"))
    return render_template("register.html",title="Register",form=form)

@app.route("/login",methods=["GET","POST"])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        if form.username.data=="Admin" and form.password.data=="Administrator":
            flash('Welcome Admin!','success')
            return redirect(url_for('admin_page'))
        else:
            user=User.query.filter_by(username=form.username.data).first()
            if user and bcrypt.check_password_hash(user.password,form.password.data):
                flash('Login successful!','success')
                login_user(user,remember=form.remember.data)
                return redirect(url_for("home"))
    return render_template("login.html",title="Login",form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/admin/page',methods=['GET','POST'])
def admin_page():
    products=Product.query.all()
    categories = Category.query.all()
    form=CategoryForm()
    form_s=SearchForm()
    if form.validate_on_submit():
        ctegory=Category(c_name=form.category.data)
        db.session.add(ctegory)
        db.session.commit()
        flash('New Category added','success')
        return redirect(url_for('admin_page'))

    categories=Category.query.all()
    cat_list=[cat.c_name for cat in categories]
    form_2=ProductForm()
    form_2.catgory.choices = [(c,c) for c in cat_list]
    if form_2.validate_on_submit():
        product=Product(p_name=form_2.product.data,category=form_2.catgory.data,price=form_2.price.data,stock=form_2.stock.data,expiry_date=form_2.expiry.data)
        db.session.add(product)
        db.session.commit()
        flash('Product added!!!','success')
        return redirect(url_for('admin_page'))
    return render_template('admin_page.html',title='AdminPage',form=form,form_2=form_2,categories=categories,products=products,form_s=form_s)

@app.route('/category/<int:c_id>/edit',methods=['GET','POST'])
def c_edit(c_id):
    category_to_update=Category.query.get_or_404(c_id)
    form=UpdateCategoryForm()
    form_s=SearchForm()
    if form.validate_on_submit():
        category_to_update.c_name=form.category.data
        db.session.commit()
        flash("Your category has been updated",'success')
        return redirect(url_for('admin_page'))
    elif request.method=='GET':
        form.category.data=category_to_update.c_name
    else:
        flash("Update failed!!! please try again")
        return redirect(url_for('c_edit',c_id=category_to_update.c_id))

    return render_template("c_edit.html",title="Category Edit",category_to_update=category_to_update,form=form,form_s=form_s)



@app.route('/product/<int:p_id>/edit',methods=['GET','POST'])
def p_edit(p_id):
    product_to_update=Product.query.get_or_404(p_id)
    form_s=SearchForm()
    form=UpdateProductForm()
    if form.validate_on_submit():
        product_to_update.p_name=form.product.data
        product_to_update.price=form.price.data
        product_to_update.stock=form.stock.data
        product_to_update.expiry_date=form.expiry.data
        db.session.commit()
        flash("Your product has been updated",'success')
        return redirect(url_for('admin_page'))
    elif request.method=='GET':
        form.product.data=product_to_update.p_name
        form.price.data=product_to_update.price
        form.stock.data=product_to_update.stock
        form.expiry.data=product_to_update.expiry_date
    else:
        flash("Update failed!!! please try again")
        return redirect(url_for('p_edit',c_id=product_to_update.p_id))
    return render_template("p_edit.html",title="Product Edit",product_to_update=product_to_update,form=form,form_s=form_s)

@app.route('/delete/<int:c_id>/category')
def c_delete(c_id):
        category_to_delete = Category.query.get(c_id)
        products=Product.query.all()
        if category_to_delete:
            for product in products :
                if(product.category==category_to_delete.c_name):
                    db.session.delete(product)
            db.session.delete(category_to_delete)
            db.session.commit()
            flash("Category Deleted")
            return redirect(url_for('admin_page'))


@app.route('/delete/<int:p_id>')
def p_delete(p_id):
    product_to_delete = Product.query.get(p_id)
    db.session.delete(product_to_delete)
    db.session.commit()
    flash("Product Deleted")
    return redirect(url_for('admin_page'))


@app.route('/add-to-cart', methods=['POST'])
def add_to_cart():

    if 'cart' not in session:
        session['cart'] = []

    form = AddToCart()

    if form.validate_on_submit():

        session['cart'].append({'id' : form.id.data, 'quantity' : form.quantity.data})
        session.modified = True

    return redirect(url_for('home'))


@app.route('/cart')
@login_required
def cart():

    products = []
    grand_total = 0
    index = 0
    try:

        for item in session['cart']:
            product = Product.query.filter_by(p_id=item['id']).first()

            quantity = int(item['quantity'])
            total = quantity * product.price
            grand_total += total

            products.append({'id' : product.p_id, 'name' : product.p_name, 'price' :  product.price, 'quantity' : quantity, 'total': total, 'index': index})
            index += 1


        return render_template('cart.html', products=products, grand_total=grand_total)
    except:
        flash("Your cart is empty!!!!!",'success')
        return redirect(url_for('home'))


@app.route('/remove-from-cart/<index>')
def remove_from_cart(index):
    del session['cart'][int(index)]
    session.modified = True
    return redirect(url_for('cart'))

@app.route('/search', methods=['GET', 'POST'])
def search():
    form_s=SearchForm()
    if form_s.validate_on_submit:
        query=form_s.searched.data
        categories = Category.query.filter(Category.c_name.ilike(f"%{query}%")).all()
        products = Product.query.filter(Product.p_name.ilike(f"%{query}%")).all()
        return render_template('search_results.html', categories=categories, products=products, query=query,form_s=form_s)

@app.route('/buy')
def buy():
    flash('Your Grocerries have been ordered. Thanks for shopping!!!','success')
    return redirect(url_for('home'))




