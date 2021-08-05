import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { linedraggableComponent } from './line-draggable.component';

const routes: Routes = [{ path: '', component: linedraggableComponent }];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class linedraggableRoutingModule {}
