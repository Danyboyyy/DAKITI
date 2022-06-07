# **DAKITI**

## **Estructura del Progrma**
### Inicio del Programa
```
program <nombre_del_programa>
```
### Declaracion de Variables
#### Tipos Soportados
- int
- float
- bool
- string \
Soporta también la creación de arreglos.
```
vars
    <tipo> <nombre_variable>, <nombre_variable>, nombre_variable[<tamaño_arreglo>];
```
### Declaración de Funciones
#### Tipos Soportados
- int
- float
- bool
- string 
- void 
```
function <tipo> <nombre_funcion> () {
    <Declaración de variables locales (opcional)>

    <Estatutos>
}
```

### Cuerpo del Programa
```
main {
    <Estatutos>
}
```

## **Estatutos**
### **Expresiones, Asignación y Estatuto de Salida**
#### **Operaciones Aritméticas**
- +: suma
- -: resta
- *: multiplicación
- /: división
- %: módulo
#### **Operaciones de Comparación**
- <: menor que
- \>: mayor que
- <=: menor o igual que
- \>=: mayor o igual que
- ==: igual que
- <>: diferente que
#### **Operaciones Booleanas**
- &&: and
- ||: or
#### **Estatuto de Salida**
- print: impresión en consola
```
program test;

vars
    int x, y, res;
    bool t, f;
    string str;
    float a, b;

main {
    x = 10;
    y = 20;

    res =  x + y;
    print(res);

    t = true;
    f = x == y;
    print(f && t);

    str = "hello world";
    print(str);

    a = 10.0
    b = 2.5
    print(a / b);

}
```
### **If, else if, else**
```
if (<expresión_booleana>) {
    <Estatutos>
}
else if (<expresión_booleana>) {
    <Estatutos>
}
else {
    <Estatutos>
}
```
#### Ejemplo:
```
program test;

vars
    int x, y;

main {
    x = 10;
    y = 20;

    if (x < y) {
        print("x es menor que y");
    }
    else if (x > y) {
        print("x es mayor que y");
    }
    else {
        print("x y y son iguales");
    }

}
```
### **For y While**
```
for (<variable> in range(<límite_inferior>, <límite_superior>)) {
    <Estatutos>
}

while (expresión_booleana) {
    <Estatutos>
}
```
#### Ejemplo:
```
program test;

vars
    int i;

main {
    for (i in range(1, 10)) {
        pritn(i);
    }

    i = 1;
    while (i <= 10) {
        print(i);
    }

}
```
## **Arreglos y Funciones**
### **Manejo de Arreglos**
```
<nombre_variable>[<posición_del_arreglo>] = <expresión>
```
#### Ejemplo:
```
program test;

vars
    int arr[10], i;

main {
    for (i in range(1, 10)) {
        arr[i] = i;
    }

    for (i in range(1, 10)) {
        print(arr[i]);
    }

}
```
### **Declaración e Invocación de Funciones**
```
<nombre_función>(<nombre_variable>, <nombre_variable>);
<nombre_variable> = <nombre_función>(<nombre_variable>, <nombre_variable>);
```
#### Ejemplo:
```
program test;

vars
    string nombre, resultado;

function void imprime(string str) {
    print(str);
}

function int suma(int x, int y) {
    vars
        int res;
    res = x + y;
    return(res);
}

main {
    nombre = "Daniel";
    imprime(nombre);

    resultado = suma(10 + 5);
    print(resultado);

}
```
## **Ejemplo Fibonacci**
```
program factorial;

vars
    int n, res;

function int factorialDP(int num) {
    vars
        int i, res;

    i = 2;
    res = 1;

    while (i <= num) {
        res = res * i;
        i = i + 1;
    }

    return(res);
}

function int factorialRecursive(int num) {
    vars
        int aux;
    if (num < 0) {
        return(0);
    }
    else if (num > 1) {
        aux = num - 1;
        return(num * factorialRecursive(aux));
    }
    return(1);
}

main {
    n = 6;
    res = factorialDP(n);
    print(res);
    print("Factorial of 6 (cyclic)", factorialDP(n));
    print("Factorial of 6 (recursive)", factorialRecursive(n));
}
```