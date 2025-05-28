# src/views/widgets/donut_chart.py
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QColor, QPen, QFont
from PyQt6.QtCore import Qt, QRectF

class DonutChart(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(300, 350)  # Reduced minimum size
        self.setStyleSheet("background-color: grey;")
        self.data = []
        
    def set_data(self, category_data):
        """Set the data for the chart and trigger a repaint"""
        self.data = []
        
        color_mapping = {
            "Entertainment": "#f44336",
            "Food": "#4a86e8",
            "Groceries": "#4CAF50",
            "Healthcare": "#9C27B0",
            "Housing": "#FF9800",   
            "Shopping": "#FFEB3B",
            "Transportation": "#FF5722",
            "Utilities": "#00BCD4",
            "Other": "#9E9E9E"
        }
        
        if not category_data:  # Explicitly handle empty data
            self.update()  # Clear the chart
            return

        total = sum(category_data.values())
        if total == 0:
            self.update()
            return
            
        # Sort categories by amount in descending order
        sorted_categories = sorted(category_data.items(), key=lambda x: x[1], reverse=True)
        
        for category, amount in sorted_categories:
            percentage = (amount / total) * 100
            self.data.append({
                "value": percentage,
                "color": QColor(color_mapping.get(category, "#9E9E9E")),
                "label": category,
                "amount": f"₱{amount:.2f}"
            })
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Calculate available space for chart and legend
        padding = 20
        available_width = self.width() - 2 * padding
        available_height = self.height() - 2 * padding
        
        # Define space for legend on the right
        legend_width = 180 # Estimate needed width for legend
        
        # Calculate space for chart on the left
        chart_area_width = available_width - legend_width
        chart_area_height = available_height
        
        # Calculate chart size (square)
        chart_size = min(chart_area_width, chart_area_height)
        chart_size = max(chart_size, 100) # Ensure minimum size
        
        # Calculate chart position (centered in its area)
        chart_x = padding + (chart_area_width - chart_size) // 2
        chart_y = padding + (chart_area_height - chart_size) // 2
        
        rect = QRectF(chart_x, chart_y, chart_size, chart_size)

        if not self.data:
            painter.setBrush(QColor("#9E9E9E"))  # Gray color
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawPie(rect, 0, 360 * 16)  # Full circle
            
            # Draw center circle to create donut hole
            center = rect.center()
            hole_radius = chart_size / 4
            painter.setBrush(QColor("#FFFFFF"))
            painter.drawEllipse(center, hole_radius, hole_radius)
            
            # Draw "No Data" text in center
            font = QFont()
            font.setPointSize(12)
            painter.setFont(font)
            painter.setPen(QColor("#333333"))
            painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, "No Data")
            return
        
        total = sum(item["value"] for item in self.data) if self.data else 1
        start_angle = 0
        
        # Draw donut segments
        for item in self.data:
            sweep_angle = 360 * (item["value"] / total)
            painter.setBrush(item["color"])
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawPie(rect, int(start_angle * 16), int(sweep_angle * 16))
            start_angle += sweep_angle
        
        # Draw center circle to create donut hole
        center = rect.center()
        hole_radius = chart_size / 4
        painter.setBrush(QColor("#FFFFFF"))
        painter.drawEllipse(center, hole_radius, hole_radius)
        
        # Draw legend
        legend_start_x = padding + chart_area_width + padding # Start legend after chart area + padding
        self.draw_legend(painter, legend_start_x, padding, legend_width, available_height) # Pass legend area bounds
        
    def draw_legend(self, painter, legend_start_x, legend_start_y, legend_width, legend_height):
        painter.setPen(QColor("#333333"))
        font = QFont()
        font.setPointSize(9)  # Adjusted font size
        painter.setFont(font)
        
        item_spacing = 5 # Spacing between legend items
        item_height = 20 # Estimated height of each legend item
        
        # Calculate starting y position to center legend vertically in its area
        total_legend_height = len(self.data) * (item_height + item_spacing)
        y_pos = legend_start_y + (legend_height - total_legend_height) // 2
        
        for i, item in enumerate(self.data):
            x_pos_square = legend_start_x + 5 # Small padding from left edge of legend area
            x_pos_text = x_pos_square + 20 # Space for color square + padding
            
            # Draw color square
            painter.setBrush(item["color"])
            painter.setPen(Qt.PenStyle.NoPen)
            square_size = 12 # Size of the color square
            painter.drawEllipse(x_pos_square, y_pos + (item_height - square_size) // 2, square_size, square_size)
            
            # Draw label and amount
            painter.setPen(QColor("#333333"))
            
            label = item['label']
            amount = item['amount']
            
            # Calculate available width for text
            available_text_width = legend_width - (x_pos_text - legend_start_x) - 5 # Leave some padding on the right
            
            # Simple layout: label on the left, amount aligned to the right within the available text width
            label_rect = QRectF(x_pos_text, y_pos, available_text_width, item_height)
            painter.drawText(label_rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, label)
            
            # Calculate amount position for right alignment
            amount_rect = QRectF(x_pos_text, y_pos, available_text_width, item_height)
            painter.drawText(amount_rect, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, amount)
            
            y_pos += item_height + item_spacing