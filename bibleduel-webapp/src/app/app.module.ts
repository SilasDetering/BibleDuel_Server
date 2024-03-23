import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { NgxColorsModule } from 'ngx-colors';
import { AppRoutingModule } from './app-routing.module';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

import { AppComponent } from './app.component';
import { HomeComponent } from './components/home/home.component';
import { LoginComponent } from './components/login/login.component';
import { NavbarComponent } from './components/navbar/navbar.component';
import { FlashMessagesComponent } from './components/flash-messages/flash-messages.component';
import { UserComponent } from './components/user/user.component';
import { QuestionsComponent } from './components/questions/questions.component';
import { CategoriesComponent } from './components/categories/categories.component';
import { DashboardComponent } from './components/dashboard/dashboard.component';
import { StatisticsComponent } from './components/statistics/statistics.component';

import { AdminGuard } from './guarts/admin.guard';
import { ChangelogsComponent } from './components/changelogs/changelogs.component';

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    LoginComponent,
    NavbarComponent,
    FlashMessagesComponent,
    UserComponent,
    QuestionsComponent,
    CategoriesComponent,
    DashboardComponent,
    StatisticsComponent,
    ChangelogsComponent,  
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    HttpClientModule,
    NgxColorsModule,
    BrowserAnimationsModule,
    ReactiveFormsModule,
  ],
  providers: [
    AdminGuard,
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
