from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from shop.models import Feedback, Product
from .serializer import (
    FeedbackSerializer, FeedbackUpdateSerializer,
    AdminAnswerSerializer, AdminBlockSerializer
)
from .utils import user_ordered_product


# Добавление отзыва авторизованным пользователем на товар из своего завершенного заказа
class AddView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Добавление отзыва на товар",
        operation_description="Для авторизованных пользователей. Добавляет отзыв на товар из завершенных заказов текущего пользователя",
        request_body=FeedbackSerializer,
        responses={201: FeedbackSerializer(),
                   400: "Ошибка (невалидные параметры запроса)",
                   403: "Ошибка (попытка оставить отзыв на товар, которого нет в завершенных заказах пользователя)",
                   404: "Ошибка (данные не найдены)"
                   }
    )
    def post(self, request):
        product_id = request.data.get("product_id")
        if not product_id:
            return Response({"error": "product_id обязателен"}, status=status.HTTP_400_BAD_REQUEST)
        feedback_text = request.data.get("feedback")
        if not feedback_text:
            return Response({"error": "feedback обязателен"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Продукт не найден"}, status=status.HTTP_404_NOT_FOUND)

        if not user_ordered_product(request.user, product):
            return Response({"error": "Вы не можете оставить отзыв на этот товар"}, status=status.HTTP_403_FORBIDDEN)

        feedback = Feedback.objects.create(
            creator_id=request.user,
            product_id=product,
            feedback=feedback_text
        )
        return Response(FeedbackSerializer(feedback).data, status=status.HTTP_201_CREATED)


# Изменение отзыва авторизованным пользователем на товар из своего завершенного заказа
class UpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Редактирование отзыва на товар",
        operation_description="Для авторизованных пользователей. Позволяет изменить свой отзыв на товар из завершенных заказов текущего пользователя",
        request_body=FeedbackUpdateSerializer,
        responses={200: FeedbackSerializer(),
                   400: "Ошибка (невалидные параметры запроса)",
                   404: "Отзыв не найден",
                   }
    )
    def put(self, request):
        feedback_id = request.data.get("feedback_id")
        try:
            feedback = Feedback.objects.get(pk=feedback_id, creator_id=request.user)
        except Feedback.DoesNotExist:
            return Response({"error": "Отзыв не найден"}, status=status.HTTP_404_NOT_FOUND)

        serializer = FeedbackUpdateSerializer(feedback, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(FeedbackSerializer(feedback).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Удаление отзыва авторизованным пользователем на товар из своего завершенного заказа
class DeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Удаление отзыва на товар",
        operation_description="Для авторизованных пользователей. Позволяет удалить свой отзыв на товар из завершенных заказов текущего пользователя",
        manual_parameters=[
            openapi.Parameter('pk', openapi.IN_PATH, description="ID отзыва", type=openapi.TYPE_INTEGER)
        ],
        responses={204: "No Content",
                   404: "Отзыв не найден",
                   }
    )
    def delete(self, request, pk):
        try:
            feedback = Feedback.objects.get(pk=pk, creator_id=request.user)
            feedback.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Feedback.DoesNotExist:
            return Response({"error": "Отзыв не найден"}, status=status.HTTP_404_NOT_FOUND)


# Ответ на отзыв пользователя администратором
class AnswerByAdminView(APIView):
    permission_classes = [permissions.IsAdminUser]

    @swagger_auto_schema(
        operation_summary="Ответ администратора на отзыв на товар",
        operation_description="Для авторизованных пользователей с ролью администратора 1 уровня. Позволяет добавить ответ на отзыв пользователя",
        request_body=AdminAnswerSerializer,
        responses={200: FeedbackSerializer(),
                   400: "Ошибка (невалидные параметры запроса)",
                   404: "Отзыв не найден",
                   }
    )
    def put(self, request):
        serializer = AdminAnswerSerializer(data=request.data)
        if serializer.is_valid():
            feedback_id = serializer.validated_data["feedback_id"]
            try:
                feedback = Feedback.objects.get(pk=feedback_id)
                feedback.answer = serializer.validated_data["answer"]
                feedback.save()
                return Response(FeedbackSerializer(feedback).data)
            except Feedback.DoesNotExist:
                return Response({"error": "Отзыв не найден"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Блокировка отзыва администратором
class BlockByAdminView(APIView):
    permission_classes = [permissions.IsAdminUser]

    @swagger_auto_schema(
        operation_summary="Блокировка отзыва на товар",
        operation_description="Для авторизованных пользователей с ролью администратора 1 уровня. Позволяет заблокировать нежелательный отзыв пользователя на товар и скрыть для просмотра в каталоге",
        request_body=AdminBlockSerializer,
        responses={200: FeedbackSerializer(),
                   400: "Ошибка (невалидные параметры запроса)",
                   404: "Отзыв не найден",
                   }
    )
    def put(self, request):
        serializer = AdminBlockSerializer(data=request.data)
        if serializer.is_valid():
            try:
                feedback = Feedback.objects.get(pk=serializer.validated_data["feedback_id"])
                feedback.is_blocked = serializer.validated_data["is_blocked"]
                feedback.save()
                return Response(FeedbackSerializer(feedback).data)
            except Feedback.DoesNotExist:
                return Response({"error": "Отзыв не найден"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Получить отзывы на товар для каталога
class GetView(APIView):

    @swagger_auto_schema(
        operation_summary="Получение всех не заблокированных отзывов на товар",
        operation_description="Для всех пользователей. Возвращает все не заблокированные отзывы на конкретный товар для их просмотра на странице товара",
        manual_parameters=[
            openapi.Parameter('pk', openapi.IN_PATH, description="ID товара", type=openapi.TYPE_INTEGER)
        ],
        responses={200: FeedbackSerializer(many=True)}
    )
    def get(self, request, pk):
        feedbacks = Feedback.objects.filter(product_id=pk, is_blocked=False)
        return Response(FeedbackSerializer(feedbacks, many=True).data)
