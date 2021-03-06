from flask import render_template, flash, redirect, url_for, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import Required
from app import app
from werkzeug.utils import secure_filename
from app.forms import LoginForm

import os, uuid, sys
from azure.storage.blob import BlockBlobService, PublicAccess

@app.route('/')


@app.route('/questionnaire', methods=['GET', 'POST'])
def questionnaire():
    form = QuestionForm()
    if form.validate_on_submit():
        companyName = form.companyName.data
        message = "Welcome"+ companyName
        return render_template('questionnaire.html', form=form, message=message)
    else:
        return render_template('questionnaire.html', form=form)



@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))  
    return render_template('login.html', title='Sign In', form=form)

@app.route('/upload')
def upload_file():
   return render_template('upload.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def uploader():
   if request.method == 'POST':

      uploaded_files = request.files.getlist('file')
      #f = request.files['file']
      for f in uploaded_files:
          uploadToBlob(f)
    
      # List the blobs in the container
    #   print("\nList blobs in the container")
    #   generator = block_blob_service.list_blobs(container_name)
    #   for blob in generator:
    #     print("\t Blob name: " + blob.name)

      return 'file uploaded successfully'

def uploadToBlob(f):
    filename = secure_filename(f.filename)
    filepath = os.path.join('./tempdata',filename)
    f.save(filepath)


    #test test test
    # Create the BlockBlockService that is used to call the Blob service for the storage account
    block_blob_service = BlockBlobService(account_name='cs4100a111d8e55x43e5xb14', account_key='HY6YCXWTPcNMYM4yWYiXKKrKWUlpB2f2680P9hqjOopnoYiCjNIScRedkf8kBl2oUn6TES5u8JUCTIBCM6lwRw==')
    # Create a container called 'quickstartblobs'.
    container_name ='quickstartblobs'
    block_blob_service.create_container(container_name)

    # Set the permission so the blobs are public.
    block_blob_service.set_container_acl(container_name, public_access=PublicAccess.Container)

    # Upload the file to blob, use filename for the blob name.
    block_blob_service.create_blob_from_path(container_name, filename, filepath)

    # Remove the temporary files from ./data now that they are uploaded onto blob storage.
    os.remove(filepath)

class QuestionForm(FlaskForm):
    companyName = StringField('Company name:', validators=[Required()])
    industry = SelectField(u'Industry', choices=[('mining', 'Mining'),('retail', 'Retail'),
    ('forestry', 'Forestry'),('agriculture', 'Agriculture'),('construction', 'Construction')])
    companySize = SelectField(u'Company Size', choices=[('xs','1-10'),('s','10-50'),('m','50-250'),('l','250-100'),('xl','1000+')])
    submit = SubmitField('Submit')