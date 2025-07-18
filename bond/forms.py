from django import forms
from .models import Anuncio

class AnuncioForm(forms.ModelForm):
    class Meta:
      
        model = Anuncio
        fields = [
            'nome', 'memoria', 'camera', 'armazenamento', 'bateria',
            'bv_desc', 'descricao', 'marca', 'condicao', 'valor'
        ]
    
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'block w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 transition duration-200'
            }),
            'memoria': forms.NumberInput(attrs={
                'placeholder': 'Ex: 8, 12, 16',
                'class': 'block w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 transition duration-200',
                'min': '1'
            }),
            'camera': forms.NumberInput(attrs={
                'placeholder': 'Ex: 48, 108, 200',
                'class': 'block w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 transition duration-200',
                'min': '1'
            }),
            'armazenamento': forms.NumberInput(attrs={
                'placeholder': 'Ex: 128, 256, 512',
                'class': 'block w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 transition duration-200',
            }),
            'bateria': forms.NumberInput(attrs={
                'placeholder': 'Ex: 4000, 5000',
                'class': 'block w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 transition duration-200',
                'min': '1'
                
            }),
            'bv_desc': forms.TextInput(attrs={
                'placeholder': 'Ex: Novo, Lacrado, com NF.',
                'class': 'block w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 transition duration-200'
            }),
            'descricao': forms.Textarea(attrs={
                'rows': 6,
                'placeholder': 'Descreva seu celular, incluindo acessórios, histórico de uso, e quaisquer observações importantes.',
                'class': 'block w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 transition duration-200'
            }),
            'valor': forms.NumberInput(attrs={
                'placeholder': 'Ex: 2999.00',
                'step': '0.01', # Permite valores decimais
                'class': 'block w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 transition duration-200'
            }),
            'marca': forms.Select(attrs={
                'class': 'block w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 transition duration-200'
            }),
            'condicao': forms.Select(attrs={
                'class': 'block w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 transition duration-200'
            }),

        }
        
def clean_nome(self):
        nome = self.cleaned_data.get('nome', '')
        return nome.strip().strip('"').strip("'")  # remove aspas e espaço