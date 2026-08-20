<?php

namespace App\Jobs;

use App\Models\CourseCompletion;
use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Bus\Dispatchable;

class SendCompletionCertificate implements ShouldQueue
{
    use Dispatchable;
    use Queueable;

    public function __construct(public int $completionId)
    {
    }

    public function handle(): void
    {
        $completion = CourseCompletion::findOrFail($this->completionId);

        // Renders and mails the PDF certificate for a finished course.
        report_certificate_generated($completion->id);
    }
}
