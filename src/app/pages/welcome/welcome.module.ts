import { NgModule } from '@angular/core';
import { SharedModule } from '../../shared/shared.module';
import { WelcomeRoutingModule } from './welcome-routing.module';
import { WelcomeComponent } from './welcome.component';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from "@angular/common";

@NgModule({
  imports: [WelcomeRoutingModule, SharedModule, HttpClientModule, FormsModule, ReactiveFormsModule, CommonModule],
  declarations: [WelcomeComponent],
  bootstrap: [WelcomeComponent],
})
export class WelcomeModule {}
