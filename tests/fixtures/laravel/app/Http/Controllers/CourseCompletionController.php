<?php

namespace App\Http\Controllers;

use App\Http\Resources\CourseCompletionResource;
use App\Models\CourseCompletion;
use App\Services\CourseCompletionService;
use Illuminate\Http\Request;

class CourseCompletionController extends Controller
{
    public function __construct(private CourseCompletionService $completions)
    {
    }

    public function index(Request $request)
    {
        return CourseCompletionResource::collection(
            CourseCompletion::where('user_id', $request->user()->id)->get()
        );
    }

    public function complete(Request $request, CourseCompletion $completion)
    {
        $this->authorize('update', $completion);

        return new CourseCompletionResource(
            $this->completions->complete($completion)
        );
    }
}
