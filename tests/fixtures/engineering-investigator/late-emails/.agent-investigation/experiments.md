# Experiments

## Experiment 1 — is the provider delivering slowly?
Question   Does the delay happen before or after the provider accepts the message?
Method     Compare our `job_finished` send timestamps against the customer-supplied
           email header timestamps for five affected orders.
Predicts   H1 → our send is on time, the header is late
           everything else → our send is already late
Observed   Our send timestamps are themselves 28–34 min after the order; header
           timestamps follow within seconds of our send.
Result     H1 disproven (E3).

## Experiment 2 — are the emails enqueued late?
Question   Does the order flow enqueue the job promptly?
Method     Compare `job_enqueued` timestamps against order creation for 40 orders,
           20 delayed and 20 on time.
Predicts   H2 → delayed orders enqueue late
Observed   All 40 enqueue within ~1 s of order creation.
Result     H2 disproven (E4).
