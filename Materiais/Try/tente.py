try:
    numeros = [10, 20, 30, 40, 50]
    entrada = int(input("Digite um índice: "))
    print(f"O elemento no índice {entrada} é {numeros[entrada]}")
    
except Exception as e:
    print(f'Ocorreu um erro: "{e}"')
    print(f'O indice deve ser até {len(numeros)}')
    print()

else:
    print("O Programa rodou beleza!")

finally:
    print("Fim.")