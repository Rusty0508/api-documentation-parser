# Fleethand API Endpoints

Сгенерировано: 2025-09-04 11:07:19
Всего endpoints: 121

## Activities

### POST /api/activities/assign

**Описание:** API endpoint

**Параметры:**
- `https` (string) - //api-preprod.fleethand.com Please contact your sales manager to
- `key` (string) - Please contact your sales manager to
- `id` (string) - Please contact your sales manager to

---

### POST /api/activities

**Описание:** API endpoint

---

### GET /api/activities

**Описание:** activities:

---

### GET /api/activities/activity

**Описание:** largestActivityId

---

### GET /api/activities/file-pdf

**Описание:** API endpoint

---

### POST /api/activities/files

**Описание:** API endpoint

---

### GET /api/tacho/driver-activities

**Описание:** API endpoint

**Параметры:**
- `2020` (string) - 01-08T11:17:20Z).
- `2020` (string) - 01-08T11:17:20Z).

---

## Documents

### GET /api/documents/expenses

**Описание:** API endpoint

---

### GET /api/documents/trip

**Описание:** API endpoint

---

### POST /api/documents/forms/confirm

**Описание:** API endpoint

---

### POST /api/documents/forms/fill-form

**Описание:** API endpoint

---

### GET /api/documents/forms/file-pdf

**Описание:** API endpoint

---

### POST /api/documents/forms

**Описание:** API endpoint

---

### GET /api/documents/forms/form

**Описание:** API endpoint

---

### GET /api/documents/forms

**Описание:** API endpoint

---

### POST /api/documents/forms/reject

**Описание:** API endpoint

---

### POST /api/documents/forms/reject-documents

**Описание:** API endpoint

**Параметры:**
- `2020` (string) - 01-08T11:17:20Z).
- `2020` (string) - 01-09T11:17:20Z).

---

### POST /api/documents/forms/reject-documents-by-codes

**Описание:** API endpoint

**Параметры:**
- `2020` (string) - 01-08T11:17:20Z).
- `2020` (string) - 01-09T11:17:20Z).

---

## Drivers

### PUT /api/ddd/cancel-driver

**Описание:** API endpoint

---

### GET /api/ddd/driver-file/download

**Описание:** API endpoint

---

### GET /api/ddd/drivers-status

**Описание:** API endpoint

**Параметры:**
- `month` (string) - JANUARY, FEBRUARY, MARCH, APRIL,

---

### GET /api/ddd/all-drivers/download

**Описание:** API endpoint

**Параметры:**
- `month` (string) - JANUARY, FEBRUARY, MARCH, APRIL,

---

### GET /api/ddd/all-drivers/download-period

**Описание:** API endpoint

**Параметры:**
- `month` (string) - JANUARY, FEBRUARY, MARCH, APRIL,

---

### PUT /api/ddd/init-driver

**Описание:** API endpoint

**Параметры:**
- `2025` (string) - 01-
- `08T11` (string) - 17:20Z).
- `2025` (string) - 01-
- `08T11` (string) - 17:20Z).

---

### POST /api/ddd/upload-drivers

**Описание:** API endpoint

**Параметры:**
- `2020` (string) - 01-08T11:17:20Z).
- `2020` (string) - 01-09T11:17:20Z).

---

### POST /api/document/driver

**Описание:** API endpoint

**Параметры:**
- `values` (string) - DECLARATION,
- `Alpha` (string) - 2 code)

---

### GET /api/document/driver

**Описание:** API endpoint

---

### DELETE /api/document/driver

**Описание:** API endpoint

---

### GET /api/driver

**Описание:** API endpoint

---

### GET /api/eco/driver

**Описание:** API endpoint

**Параметры:**
- `2020` (string) - 01-21).
- `2020` (string) - 01-21).

---

### GET /api/tacho/driver-faults

**Описание:** API endpoint

**Параметры:**
- `2020` (string) - 01-21).
- `2020` (string) - 01-21).

---

### GET /api/driver/driver-hours

**Описание:** API endpoint

**Параметры:**
- `2020` (string) - 01-08T11:17:20Z).
- `2020` (string) - 01-08T11:17:20Z).
- `01` (string) - 30:00.000).

---

## General

### GET /api/country-change/crossings

**Описание:** API endpoint

**Параметры:**
- `2020` (string) - 01-08T11:17:20Z).
- `2020` (string) - 01-09T11:17:20Z).

---

### GET /api/country-change

**Описание:** API endpoint

**Параметры:**
- `2020` (string) - 01-08T11:17:20Z).
- `2020` (string) - 01-09T11:17:20Z).

---

### GET /api/ddd/cards

**Описание:** API endpoint

---

### GET /api/ddd/companies

**Описание:** API endpoint

**Параметры:**
- `month` (string) - JANUARY, FEBRUARY, MARCH, APRIL,

---

### GET /api/ddd/info

**Описание:** API endpoint

**Параметры:**
- `month` (string) - JANUARY, FEBRUARY, MARCH, APRIL,

---

### POST /api/geo-zones/crossing

**Описание:** API endpoint

**Параметры:**
- `2020` (string) - 01-08T11:17:20Z).
- `2020` (string) - 01-09T11:17:20Z).

---

### POST /api/integrations/sent-state

**Описание:** API endpoint

---

### GET /api/latest-panic-button

**Описание:** API endpoint

**Параметры:**
- `2020` (string) - 01-08T11:17:20Z).
- `2020` (string) - 01-09T11:17:20Z).
- `Types` (string) - GAS_TANK_OPEN,
- `types` (string) - ENGINE_OIL, ENGINE_OIL_TEMPERATURE,

---

### GET /api/alarms

**Описание:** API endpoint

**Параметры:**
- `2020` (string) - 01-08T11:17:20Z).
- `2020` (string) - 01-09T11:17:20Z).
- `Types` (string) - GAS_TANK_OPEN,
- `types` (string) - ENGINE_OIL, ENGINE_OIL_TEMPERATURE,

---

### GET /api/latest-alarms

**Описание:** API endpoint

---

### GET /api/latest-doors-info

**Описание:** API endpoint

---

### GET /api/latest-info

**Описание:** API endpoint

---

### GET /api/latest-tacho

**Описание:** API endpoint

---

### POST /api/orders

**Описание:** API endpoint

---

### GET /api/orders/actions

**Описание:** API endpoint

---

### GET /api/orders/status

**Описание:** API endpoint

---

### GET /api/orders

**Описание:** API endpoint

---

### DELETE /api/orders

**Описание:** API endpoint

---

### DELETE /api/poi/poiId

**Описание:** API endpoint

---

### DELETE /api/poi-group/poiGroupId

**Описание:** API endpoint

---

### POST /api/pois

**Описание:** API endpoint

---

### POST /api/poi-group

**Описание:** API endpoint

**Параметры:**
- `2020` (string) - 01-08T11:17:20Z).
- `2020` (string) - 01-09T11:17:20Z).

---

### GET /api/tacho/current

**Описание:** activityType

---

### GET /api/period-tacho

**Описание:** API endpoint

**Параметры:**
- `2020` (string) - 01-21).
- `2020` (string) - 01-21).

---

### GET /api/trips/statistics

**Описание:** API endpoint

**Параметры:**
- `2020` (string) - 01-08T11:17:20Z).
- `2020` (string) - 01-08T11:17:20Z).

---

### GET /api/country-change/presence

**Описание:** API endpoint

**Параметры:**
- `2020` (string) - 01-08T11:17:20Z).
- `2020` (string) - 01-09T11:17:20Z).

---

### GET /api/period-info

**Описание:** API endpoint

**Параметры:**
- `2020` (string) - 01-08T11:17:20Z).
- `2020` (string) - 01-09T11:17:20Z).

---

## Locations

### GET /api/latest-position

**Описание:** API endpoint

---

## Partners

### POST /api/partner

**Описание:** API endpoint

---

### POST /api/partner/employee

**Описание:** API endpoint

---

### DELETE /api/partner

**Описание:** API endpoint

---

### DELETE /api/partner/employee

**Описание:** API endpoint

---

## Reports

### POST /api/eco/append-to-group

**Описание:** API endpoint

**Параметры:**
- `2020` (string) - 01-21).
- `2020` (string) - 01-21).

---

### GET /api/eco/groups

**Описание:** API endpoint

---

### GET /api/report/day-country

**Описание:** API endpoint

**Параметры:**
- `2020` (string) - 01-08T11:17:20Z).
- `2020` (string) - 01-09T11:17:20Z).

---

### GET /api/report/period-summary

**Описание:** API endpoint

**Параметры:**
- `2020` (string) - 01-08T11:17:20Z).
- `2020` (string) - 01-09T11:17:20Z).
- `options` (string) - DAY, COUNTRY,

---

### GET /api/report/period-tolls

**Описание:** API endpoint

**Параметры:**
- `2020` (string) - 01-08T11:17:20Z).
- `2020` (string) - 01-09T11:17:20Z).

---

## Tasks

### POST /api/documents/task-form

**Описание:** API endpoint

---

### DELETE /api/documents/task-form

**Описание:** API endpoint

**Параметры:**
- `2020` (string) - 01-08T11:17:20Z).
- `2020` (string) - 01-09T11:17:20Z).

---

### POST /api/tasks

**Описание:** API endpoint

---

### POST /api/tasks/file

**Описание:** API endpoint

---

### POST /api/tasks/assign-trips

**Описание:** API endpoint

---

### POST /api/tasks/confirm-task

**Описание:** API endpoint

---

### POST /api/tasks/confirm-all

**Описание:** API endpoint

---

### POST /api/tasks/delete-all

**Описание:** API endpoint

---

### DELETE /api/tasks

**Описание:** API endpoint

---

### DELETE /api/tasks/trip

**Описание:** API endpoint

---

### GET /api/tasks/additional-info

**Описание:** API endpoint

---

### GET /api/tasks/done

**Описание:** === Страница 232 ===

**Параметры:**
- `2020` (string) - 01-08T11:17:20Z).
- `2020` (string) - 01-08T11:17:20Z).

---

### GET /api/tasks/eta

**Описание:** API endpoint

---

### GET /api/external-tasks/external-orders

**Описание:** API endpoint

---

### GET /api/tasks/information

**Описание:** API endpoint

**Параметры:**
- `2020` (string) - 01-08T11:17:20Z).
- `2020` (string) - 01-08T11:17:20Z).

---

### GET /api/tasks/queue

**Описание:** API endpoint

---

### GET /api/tasks/status-intervals

**Описание:** API endpoint

**Параметры:**
- `2020` (string) - 01-08T11:17:20Z).

---

### GET /api/tasks/status

**Описание:** API endpoint

---

### GET /api/tasks/trip

**Описание:** API endpoint

---

### PUT /api/tasks/mark-as-done

**Описание:** API endpoint

---

### PUT /api/tasks/mark-as-executing

**Описание:** API endpoint

---

### PUT /api/tasks

**Описание:** API endpoint

---

### POST /api/tasks/update/file

**Описание:** API endpoint

---

### POST /api/tasks/trip

**Описание:** API endpoint

---

## Users

### GET /api/user-actions

**Описание:** API endpoint

---

## Vehicles

### PUT /api/ddd/cancel-vehicle

**Описание:** API endpoint

---

### GET /api/ddd/vehicle-file/download

**Описание:** API endpoint

---

### GET /api/ddd/vehicles-status

**Описание:** API endpoint

**Параметры:**
- `month` (string) - JANUARY, FEBRUARY, MARCH, APRIL,

---

### GET /api/ddd/all-vehicles/download

**Описание:** API endpoint

**Параметры:**
- `2023` (string) - 01-21).
- `2023` (string) - 05-21).

---

### GET /api/ddd/all-vehicles/download-period

**Описание:** API endpoint

**Параметры:**
- `month` (string) - JANUARY, FEBRUARY, MARCH, APRIL,

---

### PUT /api/ddd/init-vehicle

**Описание:** API endpoint

**Параметры:**
- `2020` (string) - 01-08T11:17:20Z).
- `2020` (string) - 01-09T11:17:20Z).

---

### POST /api/ddd/upload-vehicles

**Описание:** API endpoint

---

### POST /api/document/vehicle

**Описание:** API endpoint

---

### GET /api/document/vehicle

**Описание:** API endpoint

---

### DELETE /api/document/vehicle

**Описание:** API endpoint

---

### GET /api/eco/vehicle

**Описание:** API endpoint

**Параметры:**
- `2020` (string) - 01-21).
- `2020` (string) - 01-21).

---

### POST /api/partner/vehicles

**Описание:** API endpoint

---

### DELETE /api/partner/vehicles

**Описание:** API endpoint

---

### GET /api/partner/vehicles

**Описание:** API endpoint

---

### GET /api/payment-card/vehicle

**Описание:** API endpoint

---

### POST /api/payment-card/vehicle

**Описание:** API endpoint

---

### PUT /api/payment-card/vehicle

**Описание:** API endpoint

---

### DELETE /api/payment-card/vehicle

**Описание:** API endpoint

---

### PUT /api/vehicle/deactivate

**Описание:** API endpoint

---

### GET /api/vehicle

**Описание:** API endpoint

---

### PUT /api/vehicle/update-vehicle-info

**Описание:** API endpoint

---

### PUT /api/vehicle/simple-update-vehicle-info

**Описание:** API endpoint

---

### GET /api/vehicles-group

**Описание:** API endpoint

---

### POST /api/vehicles-group

**Описание:** API endpoint

---

### PUT /api/vehicles-group/add-vehicles

**Описание:** API endpoint

---

### PUT /api/vehicles-group/remove-vehicles

**Описание:** API endpoint

---

### DELETE /api/vehicles-group

**Описание:** API endpoint

---

