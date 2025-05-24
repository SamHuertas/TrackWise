# src/views/widgets/donut_chart.py
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QColor, QPen, QFont
from PyQt6.QtCore import Qt, QRectF

class DonutChart(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(400, 450)
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
        available_height = self.height() - 40 # Consider some top and bottom padding
        min_legend_height = 60 # Estimate minimum height needed for legend (e.g., 2 lines * 30px height)
        
        # Calculate chart size based on minimum dimension, leaving space for legend
        chart_size = min(self.width() - 40, available_height - min_legend_height, 250) # Also keep a max size limit
        chart_size = max(chart_size, 100) # Ensure a minimum chart size
        
        # Calculate chart position to center it horizontally and place it above the legend area
        chart_x = (self.width() - chart_size) // 2  # Center horizontally
        chart_y = (available_height - min_legend_height - chart_size) // 2 + 20 # Center vertically above legend area with top padding
        
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
        legend_y = chart_y + chart_size
        self.draw_legend(painter, legend_y)
        
    def draw_legend(self, painter, legend_start_y):
        painter.setPen(QColor("#333333"))
        font = QFont()
        font.setPointSize(10)
        painter.setFont(font)
        
        # Start legend below the chart with some spacing
        y_start = legend_start_y + 30
        
        # Calculate how many items per row (3 columns)
        items_per_row = 3
        
        # Calculate the total width available for the legend items, considering padding
        available_width = self.width() - 40  # 20 pixels padding on each side
        
        # Calculate the width of each column segment
        column_segment_width = available_width // items_per_row
        
        for i, item in enumerate(self.data):
            row = i // items_per_row
            col = i % items_per_row
            
            # Calculate x_pos for the start of the current column segment
            segment_start_x = 20 + col * column_segment_width
            
            # Position the color square and text within this segment
            # Add a small offset from the segment start for padding
            x_pos = segment_start_x + 5
            
            y_pos = y_start + (row * 30)
            
            # Draw color square
            painter.setBrush(item["color"])
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(x_pos, y_pos, 15, 15)
            
            # Draw label and amount
            painter.setPen(QColor("#333333"))
            
            # Calculate positions relative to the start of the column segment
            label_x = segment_start_x + 25 # Offset from segment start
            amount_x = segment_start_x + column_segment_width - 60 # Position amount near the end of the segment
            
            # Ensure amount_x is not too close to label_x
            if amount_x < label_x + 80: # Assuming a max label width of around 80 pixels
                amount_x = label_x + 80

            painter.drawText(label_x, y_pos + 12, 
                           f"{item['label']}")
            painter.drawText(amount_x, y_pos + 12, 
                           f"{item['amount']}")