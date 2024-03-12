import { Component, OnInit, Input, EventEmitter, Output } from '@angular/core';
import { Category } from 'src/app/models/category.model';
import { CategorieService } from 'src/app/services/categorie.service';
import { FlashMessageService } from 'src/app/services/flash-messages.service';

@Component({
  selector: 'app-categories',
  templateUrl: './categories.component.html',
  styleUrl: './categories.component.css'
})
export class CategoriesComponent implements OnInit{

  constructor(
    private categorieService: CategorieService,
    private flashMessage: FlashMessageService,
  ) { }

  @Input() category_list: Category[] = [];
  @Output() refresh = new EventEmitter<boolean>();

  categorie_delete: Category | undefined;
  selected_categorie: Category | undefined;

  new_category = {
    title: "",
    subtitle: "",
    color: "#505050",
    timelimit: 0,
  };

  ngOnInit() {
    this.category_list.sort((a, b) => a.title.localeCompare(b.title));
  }

  onSort(event: Event) {
    const selectedOption = (event.target as HTMLSelectElement).value;
    switch (selectedOption) {
      case 'Alphabetisch':
        this.category_list.sort((a, b) => a.title.localeCompare(b.title));
        break;
      case 'anz. Fragen absteigend':
        this.category_list.sort((a, b) => b.question_count - a.question_count);
        break;
      case 'anz. Fragen aufsteigend':
        this.category_list.sort((a, b) => a.question_count - b.question_count);
        break;
      default:
        break;
    }
  }

  abbord_new_category(){
    this.new_category = {title: "", subtitle: "", color: "#505050", timelimit: 0};
  }

  onSelect(categorie: Category){
    console.log(this.category_list)
    this.selected_categorie = Object.assign({}, categorie);
  }

  onDelete(){
    if(this.categorie_delete){
      this.categorieService.deleteCategorie(this.categorie_delete._id).subscribe({
        next: data => {
          this.flashMessage.show(data.msg, {cssClass: 'alert-success', timeout: 5000});
          this.refresh.emit(true);
        },
        error: error => {
          this.flashMessage.show(error.message, {cssClass: 'alert-danger', timeout: 5000});
        }
      });
    }
  }

  onSaveNewCategory(){
    if(this.new_category.title && this.new_category.subtitle && this.new_category.color && this.new_category.title != "#505050"){
      const new_category_obj = new Category("0", this.new_category.title, this.new_category.subtitle, "", this.new_category.color, 0);

      this.categorieService.newCategorie(new_category_obj).subscribe({
        next: data => {
          this.flashMessage.show(data.msg, {cssClass: 'alert-success', timeout: 5000});
          this.refresh.emit(true);
          this.new_category = {title: "", subtitle: "", color: "#505050", timelimit: 0};
        },
        error: error => {
          this.flashMessage.show(error.message, {cssClass: 'alert-danger', timeout: 5000});
        }
      });
    } else {
      this.flashMessage.show('Please fill all fields', {cssClass: 'alert-danger', timeout: 5000});
    }
  }

  onSaveEditCategory(){
    if(this.selected_categorie && this.selected_categorie.title && this.selected_categorie.subtitle && this.selected_categorie.color && this.selected_categorie.title != "#505050"){
      const new_category_obj = new Category(this.selected_categorie._id, this.selected_categorie.title, this.selected_categorie.subtitle, "", this.selected_categorie.color, 0);

      this.categorieService.editCategorie(new_category_obj).subscribe({
        next: data => {
          this.flashMessage.show(data.msg, {cssClass: 'alert-success', timeout: 5000});
          this.refresh.emit(true);
        },
        error: error => {
          this.flashMessage.show(error.message, {cssClass: 'alert-danger', timeout: 5000});
        }
      });
    } else {
      this.flashMessage.show('Please fill all fields', {cssClass: 'alert-danger', timeout: 5000});
    }
  }
}
