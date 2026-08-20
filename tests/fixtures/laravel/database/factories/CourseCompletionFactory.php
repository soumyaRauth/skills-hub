<?php

namespace Database\Factories;

use App\Models\CompletionStatus;
use Illuminate\Database\Eloquent\Factories\Factory;

class CourseCompletionFactory extends Factory
{
    public function definition(): array
    {
        return [
            'status' => CompletionStatus::IN_PROGRESS,
            'completed_at' => null,
        ];
    }

    public function completed(): static
    {
        return $this->state(fn () => [
            'status' => 'completed',
            'completed_at' => now(),
        ]);
    }
}
