import { NgModule } from '@angular/core';
import { SharedModule } from '../../../../shared/shared.module';
import { linedraggableRoutingModule } from './line-draggable-routing.module';
import { linedraggableComponent } from './line-draggable.component';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule, ReactiveFormsModule } from '@angular/forms'

@NgModule({
  imports: [linedraggableRoutingModule, SharedModule, HttpClientModule, FormsModule, ReactiveFormsModule],
  declarations: [linedraggableComponent],
  bootstrap: [linedraggableComponent],
})
export class WelcomeModule {}
