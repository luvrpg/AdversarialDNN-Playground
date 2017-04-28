from webapp import app
from flask import render_template, request
from os import listdir

import json

from webapp.models import l1_model, linf_model

@app.route('/')
@app.route('/index')
def index():
  return render_template('index.html', title='Home')

@app.route('/jsma')
def jsma():
  mnist_filename='./webapp/models/mnist-model.meta'
  l1_model.setup(mnist_filename)
  return render_template('jsma.html', title='JSMA')
  
@app.route('/l_inf')
def l_inf():
  mnist_filename='./webapp/models/mnist-model.meta'
  linf_model.setup(mnist_filename)
  return render_template('fastgradientsign.html', title='L_infinity Norm')
  
@app.route('/fjsma')
def fjsma_handler():
  mnist_filename='./webapp/models/mnist-model.meta'
  l1_model.setup(mnist_filename)
  return render_template('fjsma.html', title='FJSMA')
  
@app.route('/run_adversary', methods=['POST'])
def run_adversary():
  print('Starting adversary generation')
  model_name    = request.form['model_name']
  
  if model_name == 'L1':
    # Perform tensor flow request
    upsilon_value = request.form['upsilon_value']
    sample_value  = request.form['sample']
    target_value  = int(request.form['target'])
    print('Performing the L1 attack from {} to {}'.format(sample_value, target_value))
    adversary_class = l1_model.l1_attack(sample_value, target_value, upsilon_value)
    #return "Model:{}\nUpsilon:{}".format(request.form['model_name'], request.form['upsilon_value'])
  if model_name == 'fjsma':
    # Perform tensor flow request
    upsilon_value = request.form['upsilon_value']
    sample_value  = request.form['sample']
    target_value  = int(request.form['target'])
    print('Performing the fjsma L1 attack from {} to {}'.format(sample_value, target_value))
    adversary_class = l1_model.l1_attack(sample_value, target_value, upsilon_value, fast=True)

  elif model_name =='Linf':
    epsilon_value = request.form['epsilon_value']
    sample_value  = request.form['sample']
    adversary_class = linf_model.fgsm(sample_value, epsilon_value)
    
    print('New adversary is classified as {}'.format(adversary_class))
  ret_val = {'adversary_class':str(adversary_class)}
  return json.dumps(ret_val)
    
