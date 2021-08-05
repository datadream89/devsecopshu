import { Component, OnInit } from '@angular/core';
import { NgForm } from '@angular/forms';
import { DataService } from './data.service';
import { RestService } from './rest.service';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { FormBuilder, FormGroup} from "@angular/forms";

@Component({
  selector: 'app-line-draggable',
  templateUrl: './line-draggable.component.html',
  styleUrls: ['./line-draggable.component.css'],
})
export class linedraggableComponent {
  descriptions: JSON | undefined;
  options: string[] = [];
  newrules: JSON | undefined;
  currents: string[] = [];
  selectedOptions: string;
  cloudStore: FormGroup|any;
  constructor(private dataService: DataService, private restService: RestService,private httpClient: HttpClient, public fb: FormBuilder) {
    this.cloudStore = this.fb.group({
      cde: [''],
      rulename: [''],
      regex_pattern: [''],
      regex_description: ['']


    })
  }
  isSubmit: boolean;
  isDelete: boolean;
  isRule: boolean;
  show: string;
  ngOnInit() {
    this.isSubmit = false;
    this.isDelete = false;
    this.isRule = false;
    this.show="show rules"
    this.dataService.sendGetRequest().subscribe((data) => {
      console.log(data);
      this.descriptions = data as JSON;
      this.options = Object.values(this.descriptions)[0];
      console.log(this.options)
    })
    

}

  submitForm() {
    var formData: any = new FormData();
    formData.append("cde", this.cloudStore.get('cde').value);
    formData.append("rulename", JSON.stringify(this.cloudStore.get('rulename').value));
    this.selectedOptions = JSON.stringify(this.cloudStore.get('rulename').value);
    formData.append("regex_pattern", this.cloudStore.get('regex_pattern').value);
    formData.append("regex_description", this.cloudStore.get('regex_description').value);
    this.httpClient.post('http://localhost:5002/apply_rules', formData).subscribe(
      (response) => console.log(response),
      (error) => console.log(error)
    )
    this.isDelete = false;
    this.isSubmit = !this.isSubmit;

  }

  submitRule() {
    var formData: any = new FormData();
    formData.append("cde", this.cloudStore.get('cde').value);
    this.httpClient.post('http://localhost:5002/existing_rules', formData).subscribe(
      (response) => this.currents = Object.values(response as JSON)[0],
      (error) => console.log(error)
    )
   
    if (this.show === 'show rules') {
      this.show = 'hide rules'
    } else {
      this.show = 'show rules'
    }
    this.isRule = !this.isRule;

  }

  deleteRules() {
    var formData: any = new FormData();
    formData.append("cde", this.cloudStore.get('cde').value);
    formData.append("rulename", JSON.stringify(this.cloudStore.get('rulename').value));
    this.httpClient.post('http://localhost:5002/delete_rules', formData).subscribe(
      (response) => console.log(response),
      (error) => console.log(error)
    )
    this.isSubmit = false;
    this.isDelete = !this.isDelete;
  }
}
