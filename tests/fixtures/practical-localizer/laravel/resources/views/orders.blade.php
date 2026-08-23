@extends('layouts.app')

@section('content')
    <h1>{{ __('messages.orders_count', ['count' => $orders->count()]) }}</h1>

    <p>{{ __('messages.welcome', ['name' => auth()->user()->name]) }}</p>

    @foreach ($orders as $order)
        <div class="order">
            <span>{{ $order->number }}</span>
            <span>${{ number_format($order->total, 2) }}</span>
            <span>{{ $order->created_at->format('m/d/Y') }}</span>

            <form method="POST" action="{{ route('orders.destroy', $order) }}">
                @csrf
                @method('DELETE')
                <button type="submit">{{ __('messages.remove_item') }}</button>
            </form>
        </div>
    @endforeach

    <a href="{{ route('login') }}">{{ __('Log in') }}</a>
@endsection
