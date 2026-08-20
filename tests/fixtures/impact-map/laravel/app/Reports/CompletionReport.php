<?php

namespace App\Reports;

use Illuminate\Support\Facades\DB;

class CompletionReport
{
    /** Completions per course for the admin dashboard. */
    public function countsByCourse(): array
    {
        return DB::select("
            SELECT course_id, COUNT(*) AS total
            FROM course_completions
            WHERE status = 'completed'
            GROUP BY course_id
        ");
    }
}
