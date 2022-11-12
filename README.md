# Aula sobre tdd com django
### Iniciar o projeto
### Instalar o django
>> pip install Django==3.1.1
start do projeto django
>> django-admin startproject setup .

### Podemos testar o projeto mesmo sem escrever nada, apenas para testar o ambiente de desenvolvimento
>> python3 manage.py test 

### Subir o servidor de test
# Temos uma classe para isso

### Vamos desenvolver uma aplicação web e para testar a aplicação é necessário subir o servidor, e queremos também esse cenário para os teste, para simular isso vamos usar a classe LiveServerTestCase

# Em setup criar um arquivo tests.py
>> from django.test import LiveServerTestCase


### Para simular a aplicação como se um usuário estivesse interagindo vamos usar selenium
>> pip install selenium
>> from selenium import webdriver

### Criar a classe responsável por testar o nosso app de animal
# Criar uma função responsável por iniciar os nossos testes, mas antes de iniciar os teste tenho algumas etapas que preciso cumprir, então vamos criar a função que fará isso.
```py

class AnimaisTestCase(LiveServerTestCase):
  
  def setUp(self):
    pass

>> python3 manage.py test 

```
# Veremos que não terá erros e que também foi executado nossa classe de teste

# Agora vamos configurar o selenium para que ele use o Google chrome ao invés do padrão safari


### Configurar o selenium para usar o Google chrome como navegador de teste
https://selenium-python.readthedocs.io/

# Instalar os drivers do selenium
https://selenium-python.readthedocs.io/installation.html#drivers

# Ver a versão do chrome --> Version 105.0.5195.125 (Official Build) (64-bit)

# Fazer o download para o SO correspondente
# unzip desse arquivos e depois adicionar o chrome driver a na raiz do projeto

# Instanciar o chrome driver na função setUp
```py
  def setUp(self):
    self.browser = webdriver.Chrome('/home/marcionm/docs_backup/Documents/projects/busca_animal_tdd_1/chromedriver')
# rodar o test
>>> python3 manage.py test
```
# Após realizar o test precisamos limpar a janela do navegador usando a função tearDown
```py
  def tearDown(self):
    self.browser.quit()
```
## Agora vamos testar se o navegador está abrindo e fechando a janela
```py
  def test_para_verificar_se_a_janela_do_browser_esta_ok(self):
    self.browser.get('https://nmultifibra.com.br/')
```

>>> python3 manage.py test

### Agora vamos criar o teste para abri a url do nosso servidor  
```py  
  def test_abre_janela_do_chrome(self):
    self.browser.get(self.live_server_url)
```
>>> python3 manage.py test

### Criar um teste para falhar
```py   
  def test_falhador(self):
    """Teste de exemplo de erro"""
    self.fail('Teste falhou deu ruim mesmo')
```
>>> python3 manage.py test

### Criar a história de usuário
```py 
  def test_buscando_um_novo_animal(self):
    """ Teste se um usuário encontra um animal na pesquisa"""
    
    # Vini, deseja encontrar um novo animal,
    # para adotar.    
  
    # Ele encontra o Busca Animal e decide usar o site,
    # porque ele vê no menu do site escrito Busca Animal.
    
    # Ele vê um campo para pesquisar animais pelo nome. 
    
    # Ele pesquisa por Leão e clica no botão pesquisar.

    # O site exibe 4 características do animal pesquisado.
   
    # Ele desiste de adotar um leão.
    
  # importar o BY em test.py
  ```
  >>> from selenium.webdriver.common.by import By


  ### Criar o app de animais
  >>> python3 manage.py startapp animais

  # Informar em setting
```py
INSTALLED_APPS = [
    'animais',
]
```
### Testando as URLs
# deletar o arquivo de test.py padrão do app e criar uma pasta para centralizar os testes, dentro da pasta test criar o __init__.py, criar o arquivo de test para as urls
test_urls.py

# Agora vamos testar se determinada requisição é atendida por uma view especifica 
```py
from django.test import TestCase --> classe mais comum para testes no django

from django.urls import reverse --> verifivar as urls que vamos testar -- identifica a url que estamos usando
from animais.views import index --> para chegar na url temos que ter um metodo na view fazendo esse meio de campo

class AnimaisURLSTestCase(TestCase):
  """Teste se a home da aplicação usa a função index da view"""
  def test_rota_url_utiliza_view_index(self):
    root = reverse('/')
    self.assertEqual(root.func, 'index')  
``` 
# Agora vamos criar na view a função index
```py
# Create your views here.
def index():
  pass
```
# Configurar as url
```py
from django.contrib import admin
from django.urls import path
from animais.views import  index

urlpatterns = [
    path('', index),
    path('admin/', admin.site.urls),
]
```
# Agora precisamos de uma ferramenta para ajustar as requisições http dentro  do nosso teste, vamos usar o Requestfactory

# Dentro do teste AnimaisURLSTestCase criar o cenário de test
# Importar RequestFactory
```py
class AnimaisURLSTestCase(TestCase):
  
  def setUp(self):
    self.factory = RequestFactory()
  
  def test_rota_url_utiliza_view_index(self):
    """Teste se a home da aplicação usa a função index da view"""
    request = self.factory.get('/'),
    response = index(request)
    self.assertEqual(response.status_code, 200)  
```  
# passar o request como parametro da view, importar o HttpResponse e retornar ele na index
```py
from django.shortcuts import render
from django.http import HttpResponse


def index(request):
  return HttpResponse()

>>> python3 manage.py test
```
# Ao realizar esse test verificamos que conseguimos realizar o ciclo corretamente, temos uma url que irá renderizar corretamente nossa index


# vamos iniciar o teste funcional
# vamos configurar o nosso teste de unidade no test_urls para ver se nossa resposta da view usa um template

### Vamos aprender usar um gerenciador de contexto a clausula with

# testar se o nosso template e chamado na view index
```py
 def test_rota_url_utiliza_view_index(self):
    """Teste se a home da aplicação usa a função index da view"""
    request = self.factory.get('/'),
    with self.assertTemplateUsed('index.html'):
      response = index(request)
      self.assertEqual(response.status_code, 200)
```
# Agora devemos prepar a view para renderizar um template
# em views.py mudar a função index
```py
from django.shortcuts import render

# Create your views here.
def index(request):
  return render(request, 'index.html')
```
# criar a pasta template
# criar o arquivo index.html
# criar um document html basic com o navbar

```html
<!DOCTYPE html>
<html lang="pt-br">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Busca Animal</title>
</head>
<body>

  <a class="navbar">Busca Animal</a>
  
</body>
</html>

```

>>> python3 manage.py test --> veremos que passou

# Agora vamos seguir com o cenário de test
# Vamos atacar agora: # Ele vê um campo para pesquisar animais pelo nome. 
# Em test_url.py 
```py
 buscar_animal_input = self.browser.find_element('input#buscar-animal')
    self.assertEqual(buscar_animal_input.get_attribute('placeholder'),'Exemplo: leão')
```
# Criar o input no html do template
```html
    <input type="text" id="buscar-animal" placeholder="Exemplo: leão, urso...">
```
>>> python3 manage.py test --> veremos que passou

# Seguindo com a história do usuário

# Ele pesquisa por Leão e clica no botão pesquisar.
# O site exibe 4 características do animal pesquisado.

### Vamos criar o cenário que um usuário digita um texto para pesquisar e clica no botão pesquisar em test.py
```py
 buscar_animal_input.send_keys('leao')
    self.browser.find_element(By.CSS_SELECTOR,'form button').click()
```

# criar o form em index.html
```html
<form>
    <input type="text" id="buscar-animal" placeholder="Exemplo: leão, urso...">
    <button type="submit">Pesquisar</button> 
  </form>
```

# Mostrar o texto sendo digitado
# em test.py 
```py
 import time
 buscar_animal_input.send_keys('leao')
 time.sleep(5)
 ```

# Continuando a história do usuário
 # O site exibe 4 características do animal pesquisado.
```py
    caracterisiticas = self.browser.find_elements(By.CSS_SELECTOR,'.result-description')
    self.assertGreater(len(caracterisiticas),3) 
```
# mudar a index.html adicionando:
```html
 <div class='result-description'>
    <div class='result-description'>
      <div class='result-description'>  
        <div class='result-description'>
  </div>
```
## Agora vamos fazer o teste e exibir as características encontradas em uma página
# temos que configurar de forma correta a view, o model que estamos renderizando de forma correta

# vamos começas com testes de unidade para nossa view
### criar o test_views.py
# !Quando enviamos uma solicitação e esperamos algo por contexto vamos usar outra propriedade no lugar do RequestFactory, vamos usar selfClient --> é um tipo de navegador ficticio onde enviamos a solicitação pra ulr e temos acesso ao response context dessa nossa requisição para garantir que a requisição está construindo a resposta correta

# Em test_views.py
```py
from django.test import TestCase, RequestFactory
from django.db.models.query import QuerySet

class IndexViewTestCase(TestCase):
  def setUp(self):
    self.factory = RequestFactory()
  def test_index_view_retorna_caracteristicas_do_animal(self):
    """Teste que verfica se a index retorna as caracterisiticas do animal pesquisado""" 
    response = self.client.get('/',
                                
        {'caracteristicas':'resultado'}
    )
    self.assertIs(type(response.context['caracteristicas']),QuerySet)
```
# Agora vamos criar as caracteristicas  
# em views.py de animal precisamos passar um context 
```py
def index(request):
  context = {'caracteristicas':None}
  return render(request, 'index.html',context)
``` 
>>> python3 manage.py test --> veremos que não passou pois a classe NoneType não é um QuerySet precisamos tornalo um.

# na view.py
```py
from django.shortcuts import render
from animais.models import Animal


# Create your views here.
def index(request):
  context = {'caracteristicas': Animal.objects.all()}
  return render(request, 'index.html',context)
```

# Criar o model e fazer apenas a makemigrations
```py
from django.db import models


# Create your models here.
class Animal(models.Model):
  pass
```  
# Agora vamos criar um model para teste
```py
from django.test import TestCase, RequestFactory

from animais.models import Animal

class AnimalModelTestCase(TestCase):
  def setUp(self):
    #criar um animal de teste
    self.animal = Animal.objects.create(
      nome_animal = 'Leão',
      predador = 'Sim',
      venenoso = 'Não',
      domestico = 'Não'  
    )
def test_animal_cadastrado_com_caracteristicas(self):
  """Teste que verifica se o animal está cadastrado com suas respectivascaracteristicas"""
  self.assertEqual(self.animal.nome_animal, 'Leão')

  ```
   
### Criar o teste para vericar a busca_animal 
Em test_view.py continuar desenvolvendo a class IndexViewTestCase 
Realizar o import do model Animal para criar uma instancia do animal

from animais.models import Animal

### instaciar
```py
    self.animal = Animal.objects.create(
      nome_animal = 'calopsita',
     predador = 'Não' ,
     venenoso = 'Não',
     domestico = 'Sim'
    )
``` 
### Mudar as caracteristicas do animal pesquisado
### Nomear na index.html o input para buscar
```html
 <input type="text" id="buscar-animal" placeholder="Exemplo: leão, urso..." name="buscar">
```
### alterar o contexto do get que será salvo em response
```py
 response = self.client.get('/',
                                
        {'buscar':'calopsita'}
    )
```
### pegar o nome desse get 

```py
caracteristica_animal_pesquisado = response.context['caracteristicas']  
```
### fazer o assertEqual
```py
self.assertEqual(caracteristica_animal_pesquisado[0].nome_animal, 'calopsita') 
``` 
### Configuar a view para que qq animal que seja pesquisado seja exibido na tela
### O site exibe 4 características do animal pesquisado.
### Criar uma instancia de teste para o animal em test.py
```py
self.animal = Animal.objects.create(
      nome_animal = 'leaõ',
      predador = 'Sim',
      venenoso = 'Não',
      domestico = 'Não'
    )
```
### Em views.py criar um contexto para o animal pesquisado
```py
def index(request):
  context = {'caracteristicas':None}
  if 'buscar' in request.GET:
    animais = Animal.objects.all()
    animal_pesquisado = request.GET['buscar']
    caracteristicas = animais.filter(nome_animal__icontains=animal_pesquisado)
    context= {'caracteristicas':caracteristicas}
    
  return render(request, 'index.html',context)
```
### Em index.html realizar a mudança para exibir de fato as características do animal pesquisado
```html
 </form>
  {% for caracteristica in caracteristicas %}
    <div class='result-description'>{{caracteristica.nome_animal}}</div>
    <div class='result-description'>{{caracteristica.predador}}</div>
    <div class='result-description'>{{caracteristica.venenoso}}</div>
    <div class='result-description'>{{caracteristica.domestico}}</div>  
  {% endfor %}
```
>>> python3 manage.py test

# Agora vamos alterar nossa app para rodar e realizar teste com animais cadastrados
### Vamos criar varios animais com lista_animais
>>> python3 lista_animais.py 

### criar a pasta static em setup
### colar o arquivo com style.css
### informar a rota dos arquivos staticos em settings.py
```py
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'setup/static')]
```
## referenciar os arquivos staticos
>>> python3 manage.py collectstatic


# tdd_busca_animal
