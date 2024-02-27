import { Component, Input } from '@angular/core';


@Component({
  selector: 'app-statistics',
  templateUrl: './statistics.component.html',
  styleUrl: './statistics.component.css'
})
export class StatisticsComponent {

  constructor() { }

  @Input() nr_of_users: number = NaN;
  @Input() nr_of_contributors: number = NaN;

  @Input() nr_of_categories: number = NaN;
  @Input() nr_of_questions: number = NaN;
  @Input() nr_of_games: number = NaN;
  @Input() nr_of_reports: number = NaN;
}
