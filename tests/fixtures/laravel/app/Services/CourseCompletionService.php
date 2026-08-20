<?php

namespace App\Services;

use App\Jobs\SendCompletionCertificate;
use App\Models\CompletionStatus;
use App\Models\CourseCompletion;

class CourseCompletionService
{
    public function complete(CourseCompletion $completion): CourseCompletion
    {
        if ($completion->status === CompletionStatus::COMPLETED) {
            return $completion;
        }

        $completion->status = CompletionStatus::COMPLETED;
        $completion->completed_at = now();
        $completion->save();

        SendCompletionCertificate::dispatch($completion->id);

        return $completion;
    }
}
