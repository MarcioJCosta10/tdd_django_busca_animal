from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from animais.models import Animal
import time

class AnimaisTestCase(LiveServerTestCase):
  
  def setUp(self):
    self.browser = webdriver.Chrome('/home/marcionm/Documents/projects/busca_animal_tdd_1/chromedriver')
    self.animal = Animal.objects.create(
      nome_animal = 'leão',
      predador = 'Sim',
      venenoso = 'Não',
      domestico = 'Não'
    )
  
  def tearDown(self):
    self.browser.quit()
    
  # def test_para_verificar_se_a_janela_do_browser_esta_ok(self):
  #   self.browser.get('https://nmultifibra.com.br/')
    
  # def test_abre_janela_do_chrome(self):
  #   self.browser.get(self.live_server_url)
    
  # def test_falhador(self):
  #   """Teste de exemplo de erro"""
  #   self.fail('Teste falhou deu ruim mesmo')    

  def test_buscando_um_novo_animal(self):
    """ Teste se um usuário encontra um animal na pesquisa"""
    
    # Vini, deseja encontrar um novo animal,
    # para adotar.  
  
    # Ele encontra o Busca Animal e decide usar o site, --> primeio vamos subir a homepage
    home_page = self.browser.get(self.live_server_url + '/')
    
    # porque ele vê no menu do site escrito Busca Animal.
    brand_element = self.browser.find_element(By.CSS_SELECTOR, '.navbar')
    self.assertEqual('Busca Animal', brand_element.text)
    
    # Ele vê um campo para pesquisar animais pelo nome. 
    buscar_animal_input = self.browser.find_element(By.CSS_SELECTOR,'input#buscar-animal')
    self.assertEqual(buscar_animal_input.get_attribute('placeholder'),'Exemplo: leão, urso...')
    
    # Ele pesquisa por Leão e clica no botão pesquisar.
    buscar_animal_input.send_keys('leão')
    time.sleep(5)
    self.browser.find_element(By.CSS_SELECTOR,'form button').click()
    
    # O site exibe 4 características do animal pesquisado.
    caracteristicas = self.browser.find_elements(By.CSS_SELECTOR,'.result-description')
    self.assertGreater(len(caracteristicas),3)
    # Ele desiste de adotar um leão.
