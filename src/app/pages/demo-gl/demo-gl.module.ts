import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NgxEchartsModule } from 'ngx-echarts';
import { SharedModule } from '../../shared/shared.module';
import { DemoGlRoutingModule } from './demo-gl-routing.module';
import { GlBar3dComponent } from './gl-bar3d/gl-bar3d.component';


@NgModule({
  declarations: [GlBar3dComponent],
  imports: [
    CommonModule,
    SharedModule,
    NgxEchartsModule,
    DemoGlRoutingModule
  ]
})
export class DemoGlModule { }
