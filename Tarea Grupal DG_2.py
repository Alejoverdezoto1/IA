
import matplotlib.pyplot as plt
import numpy as np
import random
import time
class VisualEnvironment3x3:
    def __init__(self):
        # Cuadricula 3x3: 0 = Limpio, 1 = Sucio
        self.grid = np.zeros((3, 3), dtype=int)

        # Elegir aleatoriamente entre 3 y 9 casillas sucias
        cantidad_sucias = random.randint(3, 9)
        posiciones = random.sample(range(9), cantidad_sucias)

        for posicion in posiciones:
            fila = posicion // 3
            columna = posicion % 3
            self.grid[fila, columna] = 1

        # Posicion inicial del agente
        self.agent_pos = [0, 0]

        # Consumo y estadisticas
        self.consumo = 0
        self.movimientos = 0
        self.casillas_limpiadas = 0

        # Costos energeticos
        self.costo_movimiento = 1
        self.costo_limpieza = 2

        # Configuracion del grafico
        plt.ion()
        self.fig, self.ax = plt.subplots(figsize=(6, 6))

    def render(self, step, action):
        self.ax.clear()

        # Dibujar cuadricula
        self.ax.matshow(
            self.grid,
            cmap='Blues',
            vmin=0,
            vmax=1
        )

        # Dibujar agente
        self.ax.plot(
            self.agent_pos[1],
            self.agent_pos[0],
            'ro',
            markersize=25
        )

        # Mostrar estado de las casillas
        for i in range(3):
            for j in range(3):
                estado = (
                    "SUCIO" if self.grid[i, j] == 1
                    else "LIMPIO"
                )

                self.ax.text(
                    j, i, estado,
                    ha='center',
                    va='center',
                    color='black',
                    weight='bold',
                    fontsize=9
                )

        limpias = np.sum(self.grid == 0)

        self.ax.set_title(
            f"Paso: {step} | Accion: {action}\n"
            f"Casillas limpias: {limpias}/9 | "
            f"Consumo: {self.consumo}"
        )

        self.ax.set_xticks(np.arange(-0.5, 3, 1))
        self.ax.set_yticks(np.arange(-0.5, 3, 1))
        self.ax.set_xticklabels([])
        self.ax.set_yticklabels([])
        self.ax.grid(
            which='major',
            color='black',
            linestyle='-',
            linewidth=1
        )

        plt.draw()
        plt.pause(0.5)

    def get_percept(self):
        fila, columna = self.agent_pos
        return self.agent_pos.copy(), self.grid[fila, columna]

    def execute_action(self, action):
        fila, columna = self.agent_pos

        if action == 'Suck':
            # Comprobar antes de limpiar
            if self.grid[fila, columna] == 1:
                self.grid[fila, columna] = 0
                self.consumo += self.costo_limpieza
                self.casillas_limpiadas += 1

        elif action == 'Up' and fila > 0:
            self.agent_pos[0] -= 1
            self.consumo += self.costo_movimiento
            self.movimientos += 1

        elif action == 'Down' and fila < 2:
            self.agent_pos[0] += 1
            self.consumo += self.costo_movimiento
            self.movimientos += 1

        elif action == 'Left' and columna > 0:
            self.agent_pos[1] -= 1
            self.consumo += self.costo_movimiento
            self.movimientos += 1

        elif action == 'Right' and columna < 2:
            self.agent_pos[1] += 1
            self.consumo += self.costo_movimiento
            self.movimientos += 1

    def is_completely_clean(self):
        return np.sum(self.grid) == 0



class RandomVacuumAgent:

    def __init__(self):
        # Memoria de las casillas visitadas
        self.memoria = {}

        # Recorrido sistematico en zigzag
        self.recorrido = [
            (0, 0), (0, 1), (0, 2),
            (1, 2), (1, 1), (1, 0),
            (2, 0), (2, 1), (2, 2)
        ]

        self.indice = 0

    def act(self, percept):
        pos, status = percept
        pos = tuple(pos)

        # Guardar percepcion en memoria
        self.memoria[pos] = status

        # Si esta sucia, limpiar
        if status == 1:
            return 'Suck'

        # Avanzar en el recorrido
        while self.indice < len(self.recorrido):
            objetivo = self.recorrido[self.indice]

            if pos == objetivo:
                self.indice += 1
            else:
                break

        # Finalizar cuando se completa el recorrido
        if self.indice >= len(self.recorrido):
            return 'Stop'

        objetivo = self.recorrido[self.indice]
        fila, columna = pos
        fila_obj, columna_obj = objetivo

        # Moverse hacia la siguiente casilla
        if fila < fila_obj:
            return 'Down'
        elif fila > fila_obj:
            return 'Up'
        elif columna < columna_obj:
            return 'Right'
        elif columna > columna_obj:
            return 'Left'

        return 'Stop'


if __name__ == "__main__":

    env = VisualEnvironment3x3()
    agent = RandomVacuumAgent()

    print("Cuadricula inicial:")
    print(env.grid)
    print("Casillas sucias inicialmente:", np.sum(env.grid == 1))

    env.render(step=0, action="Inicio")

    for paso in range(1, 30):
        percept = env.get_percept()
        action = agent.act(percept)

        # Detenerse al completar el recorrido
        if action == 'Stop':
            break

        env.execute_action(action)
        env.render(step=paso, action=action)

        if env.is_completely_clean():
            # La siguiente decision del agente terminara el recorrido
            # si ya se alcanzo la ultima casilla.
            pass

    print("Consumo energetico:", env.consumo)


    plt.ioff()
    plt.show()
