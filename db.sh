#!/bin/bash

ACTION=$1
ARG=$2

case "$ACTION" in
  migrate)
    if [ -z "$ARG" ]; then
      echo "❌ Please provide a migration message."
      echo "Usage: ./db.sh migrate \"add classroom table\""
      exit 1
    fi
    alembic revision --autogenerate -m "$ARG"
    ;;

  upgrade)
    alembic upgrade head
    ;;

  downgrade)
    alembic downgrade -1
    ;;

  current)
    alembic current
    ;;

  history)
    alembic history
    ;;

  reset)
    echo "⚠️  This will delete 'data/dev.db'. Are you sure? (y/n)"
    read -r confirm
    if [ "$confirm" = "y" ]; then
      rm -f data/dev.db
      echo "🗑️  Deleted dev.db"
      alembic upgrade head
      echo "✅ Database reset & migrated"
    else
      echo "❌ Aborted."
    fi
    ;;

  *)
    echo "🛠️  Usage: ./db.sh [action]"
    echo ""
    echo "Available actions:"
    echo "  migrate \"msg\"   - Create a migration with message"
    echo "  upgrade          - Apply all migrations"
    echo "  downgrade        - Revert last migration"
    echo "  current          - Show current migration"
    echo "  history          - Show migration history"
    echo "  reset            - Delete dev.db and re-run migrations"
    ;;
esac
