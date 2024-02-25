import { Component, OnInit } from '@angular/core';
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

  categorie_list: Category[] = []

  ngOnInit() {
    this.categorieService.getCategorieList().subscribe({
      next: data => {
        this.categorie_list = data.categories;
      },
      error: error => {
        this.flashMessage.show(error.message, { cssClass: 'alert-danger', timeout: 5000 });
      }
    });
  }
}
