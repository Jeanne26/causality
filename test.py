import sys
from PyQt5.QtWidgets import (
    QApplication, QGraphicsView, QGraphicsScene,
    QGraphicsEllipseItem, QGraphicsLineItem,
    QGraphicsTextItem, QMainWindow, QPushButton, QVBoxLayout, QWidget
)
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QPen
import math


class StateItem(QGraphicsEllipseItem):
    def __init__(self, name, x, y, radius=30):
        super().__init__(-radius, -radius, radius*2, radius*2)
        self.setFlag(self.ItemIsMovable)
        self.setFlag(self.ItemIsSelectable)
        self.setBrush(Qt.white)

        self.name = name
        self.text = QGraphicsTextItem(name, self)
        self.text.setPos(-10, -10)

        self.setPos(x, y)


from PyQt5.QtWidgets import QGraphicsLineItem, QGraphicsTextItem
from PyQt5.QtGui import QPen, QPolygonF
from PyQt5.QtCore import Qt, QPointF
import math


class TransitionItem(QGraphicsLineItem):
    def __init__(self, source, target, label="", weight=None):
        super().__init__()

        self.source = source
        self.target = target
        self.label = label
        self.weight = weight

        self.setPen(QPen(Qt.black, 2))

        # texte affiché
        text_str = label
        if weight is not None:
            text_str += f" ({weight})"

        self.text = QGraphicsTextItem(text_str)

        # flèche (triangle)
        self.arrow_head = QPolygonF()

        self.update_position()

    def update_position(self):
        p1 = self.source.pos()
        p2 = self.target.pos()

        self.setLine(p1.x(), p1.y(), p2.x(), p2.y())

        # position du texte
        mid_x = (p1.x() + p2.x()) / 2
        mid_y = (p1.y() + p2.y()) / 2
        self.text.setPos(mid_x, mid_y)

        # calcul angle
        angle = math.atan2(-(p2.y() - p1.y()), p2.x() - p1.x())

        arrow_size = 10

        p_arrow1 = QPointF(
            p2.x() - arrow_size * math.cos(angle + math.pi / 6),
            p2.y() + arrow_size * math.sin(angle + math.pi / 6)
        )
        p_arrow2 = QPointF(
            p2.x() - arrow_size * math.cos(angle - math.pi / 6),
            p2.y() + arrow_size * math.sin(angle - math.pi / 6)
        )

        self.arrow_head = QPolygonF([p2, p_arrow1, p_arrow2])

    def paint(self, painter, option, widget=None):
        super().paint(painter, option, widget)

        painter.setBrush(Qt.black)
        painter.drawPolygon(self.arrow_head)



class GraphEditor(QGraphicsView):
    def __init__(self):
        super().__init__()

        self.scene = QGraphicsScene()
        self.setScene(self.scene)

        self.states = []
        self.transitions = []

        self.state_count = 0
        self.selected_state = None

    def mouseDoubleClickEvent(self, event):
        pos = self.mapToScene(event.pos())
        name = f"S{self.state_count}"
        self.state_count += 1

        state = StateItem(name, pos.x(), pos.y())
        self.scene.addItem(state)
        self.states.append(state)

    def mousePressEvent(self, event):
        item = self.itemAt(event.pos())

        if event.button() == Qt.RightButton and isinstance(item, StateItem):

            # premier clic → choisir source
            if self.selected_state is None:
                self.selected_state = item
                item.setBrush(Qt.red)  # feedback visuel

            # deuxième clic → créer transition
            else:

                from PyQt5.QtWidgets import QInputDialog

                label, ok = QInputDialog.getText(self, "Transition", "Label :")
                if not ok:
                    self.selected_state.setBrush(Qt.white)
                    self.selected_state = None
                    return

                weight, ok = QInputDialog.getDouble(self, "Transition", "Poids :", 1.0, 0, 100, 2)
                if not ok:
                    self.selected_state.setBrush(Qt.white)
                    self.selected_state = None
                    return

                transition = TransitionItem(self.selected_state, item, label, weight)

                self.scene.addItem(transition)
                self.scene.addItem(transition.text)

                self.transitions.append(transition)

                # reset visuel
                self.selected_state.setBrush(Qt.white)
                self.selected_state = None

        super().mousePressEvent(event)
    def update_transitions(self):
        for t in self.transitions:
            t.update_position()

    def drawForeground(self, painter, rect):
        self.update_transitions()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.editor = GraphEditor()

        export_btn = QPushButton("Exporter vers NetworkX")
        export_btn.clicked.connect(self.export_graph)

        layout = QVBoxLayout()
        layout.addWidget(self.editor)
        layout.addWidget(export_btn)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)
        self.setWindowTitle("Éditeur LTS")

    def export_graph(self):
        lines = []
        lines.append("import networkx as nx")
        lines.append("")
        lines.append("P_graph = nx.DiGraph()")
        lines.append("")

        for t in self.editor.transitions:
            s = t.source.name
            tgt = t.target.name
            label = t.label
            weight = t.weight

            if weight is not None:
                lines.append(
                    f'P_graph.add_edge("{s}", "{tgt}", label="{label}", weight={weight})'
                )
            else:
                lines.append(
                    f'P_graph.add_edge("{s}", "{tgt}", label="{label}")'
                )

        code = "\n".join(lines)

        print("\n===== EXPORT =====\n")
        print(code)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec_())