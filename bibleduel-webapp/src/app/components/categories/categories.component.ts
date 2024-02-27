import { Component, OnInit, Input } from '@angular/core';
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

  @Input() categorie_list: Category[] = []

  ngOnInit() {
  }
}
