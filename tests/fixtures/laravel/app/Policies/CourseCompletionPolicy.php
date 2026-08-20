<?php

namespace App\Policies;

use App\Models\CourseCompletion;
use App\Models\User;

class CourseCompletionPolicy
{
    public function view(User $user, CourseCompletion $completion): bool
    {
        return $user->id === $completion->user_id;
    }

    public function update(User $user, CourseCompletion $completion): bool
    {
        return $user->id === $completion->user_id;
    }

    public function delete(User $user, CourseCompletion $completion): bool
    {
        return $user->hasRole('admin');
    }
}
