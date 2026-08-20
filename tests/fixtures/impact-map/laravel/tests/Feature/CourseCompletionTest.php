<?php

namespace Tests\Feature;

use App\Models\CompletionStatus;
use App\Models\CourseCompletion;
use Tests\TestCase;

class CourseCompletionTest extends TestCase
{
    public function test_completing_a_course_sets_the_completed_status(): void
    {
        $completion = CourseCompletion::factory()->create();

        $this->actingAs($completion->user)
            ->postJson("/api/course-completions/{$completion->id}/complete")
            ->assertOk()
            ->assertJsonPath('data.status', 'completed');

        $this->assertSame(
            CompletionStatus::COMPLETED,
            $completion->fresh()->status
        );
    }

    public function test_a_user_cannot_complete_someone_elses_course(): void
    {
        $completion = CourseCompletion::factory()->create();
        $stranger = \App\Models\User::factory()->create();

        $this->actingAs($stranger)
            ->postJson("/api/course-completions/{$completion->id}/complete")
            ->assertForbidden();
    }
}
