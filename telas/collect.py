# -*- coding: utf-8 -*-
from kivy.uix.screenmanager import Screen
#from kivy.lang import Builder


from models.senhas import Senha, Collection

from kivy.uix.button import Button

from kivy.uix.gridlayout import GridLayout
from telas.utilities import Confirma, JanelaSettings
import sys


class JanelaCollect (Screen):
    def __init__(self, smanager=None, last_window=None, **kwargs):
        super(JanelaCollect, self).__init__(**kwargs)
        
        self.last_window = last_window
        self.ids.area_collects.bind(minimum_height=self.ids.area_collects.setter('height'))
        self.smanager = smanager
        
    def recarrega (self):
        self.ids.area_collects.clear_widgets()
        cols = Collection.select()
        for c in cols:
            b = ItemColecao (c, smanager=self.smanager)
            self.ids.area_collects.add_widget(b)
            
    def on_pre_enter(self):
        self.recarrega()
    def on_leave(self):
        self.smanager.remove_widget (self)
        
    def call_settings (self):
        from telas.collect import JanelaSettings
        janela = JanelaSettings(smanager=self.smanager, name='janela_settings')
        self.smanager.add_widget( janela )
        #janela = self.smanager.get_screen('janela_add_collect')
        self.smanager.transition.direction = 'left'
        self.smanager.current = 'janela_settings'
        
    def add (self):
        from telas.collect import JanelaAddCollect
        janela = JanelaAddCollect(smanager=self.smanager, name='janela_add_collect')
        self.smanager.add_widget( janela )
        #janela = self.smanager.get_screen('janela_add_collect')
        self.smanager.transition.direction = 'left'
        self.smanager.current = 'janela_add_collect'
        
            
    def voltar (self):
        sys.exit(0)
        


class ItemColecao (Button):
    def __init__ (self, col, smanager=None, **kwargs):
        super(ItemColecao, self).__init__(**kwargs)
        self.collection = col
        self.smanager = smanager
        self.text = self.smanager.encrypter.decripta (col.nome)
        
    def on_release (self, **kwargs):
        super(ItemColecao, self).on_release(**kwargs)
        
        from telas.passwd import JanelaPassList
        janela = JanelaPassList( smanager=self.smanager, name='janela_pass_list')
        self.smanager.add_widget( janela )
        #janela = self.smanager.get_screen('janela_pass_list')
        
        janela.setup (col=self.collection)
        self.smanager.transition.direction = 'left'
        self.smanager.current = 'janela_pass_list'
        
        
        
        
class JanelaAddCollect (Screen):
    def __init__(self, smanager=None, last_window=None, **kwargs):
        super(JanelaAddCollect, self).__init__(**kwargs)
        self.last_window = last_window
        self.smanager = smanager
        
    def on_pre_enter(self):
        self.ids.espaco_superior.remove_widget (self.ids.button_deleta)
        self.ids.tx_nome.text = ''
        
    def on_leave (self):
        self.smanager.remove_widget(self)
        
    def salvar (self):
        c = Collection()
        c.nome = self.smanager.encrypter.encripta (self.ids.tx_nome.text )
        c.save()
        # Vai pra view
        #janela = self.smanager.get_screen('janela_pass_list')
        from telas.passwd import JanelaPassList
        janela = JanelaPassList( smanager=self.smanager, name='janela_pass_list')
        self.smanager.add_widget( janela )
        
        janela.setup (col=c)
        self.smanager.transition.direction = 'right'
        self.smanager.current = 'janela_pass_list'
        
    def voltar (self):
        from telas.collect import JanelaCollect
        janela = JanelaCollect(smanager=self.smanager, name='janela_collect')
        self.smanager.add_widget( janela )
        janela.recarrega()
        self.smanager.transition.direction = 'right'
        self.smanager.current = 'janela_collect'
        
    
        
        
class JanelaEditCollect (JanelaAddCollect):
    def setup (self, col):
        self.collect = col
    
    def on_pre_enter(self):
        self.ids.tx_nome.text = self.smanager.encrypter.decripta (self.collect.nome)
    
    def on_leave (self):
        self.smanager.remove_widget(self)

    def _really_delete(self, really):
        if really:
            self.collect.delete_instance(recursive=True)
            self.voltar()
            
    def delete (self):
        p = Confirma (callback=self._really_delete, text='Remover Colecao?')
        p.open()
        
        
        
    def salvar (self):
        c = self.collect
        c.nome = self.smanager.encrypter.encripta (self.ids.tx_nome.text)
        c.save()
        # Vai pra view
        #janela = self.smanager.get_screen('janela_pass_list')
        from telas.passwd import JanelaPassList
        janela = JanelaPassList( smanager=self.smanager, name='janela_pass_list')
        self.smanager.add_widget( janela )
        
        janela.setup (col=c)
        self.smanager.transition.direction = 'right'
        self.smanager.current = 'janela_pass_list'
        #self.smanager.switch_to = 'janela_pass_list'
        