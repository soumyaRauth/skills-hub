<?php

use App\Http\Controllers\CourseCompletionController;
use Illuminate\Support\Facades\Route;

Route::middleware('auth:sanctum')->group(function () {
    Route::get('/course-completions', [CourseCompletionController::class, 'index']);
    Route::post('/course-completions/{completion}/complete', [CourseCompletionController::class, 'complete']);
});
