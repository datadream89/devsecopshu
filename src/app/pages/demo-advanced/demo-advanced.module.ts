import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NgxEchartsModule } from 'ngx-echarts';
import { SharedModule } from '../../shared/shared.module';
import { DemoAdvancedRoutingModule } from './demo-advanced-routing.module';
import { AdvancedComponent } from './advanced/advanced.component';
import { ConnectChartsComponent } from './advanced/connect-charts/connect-charts.component';
import { linedraggableComponent } from './advanced/line-draggable/line-draggable.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms'

@NgModule({
  declarations: [AdvancedComponent, ConnectChartsComponent, linedraggableComponent],
  imports: [CommonModule, SharedModule, NgxEchartsModule, DemoAdvancedRoutingModule, FormsModule, ReactiveFormsModule],
})
export class DemoAdvancedModule {}
