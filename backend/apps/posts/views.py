import os
from datetime import datetime

from django.db.models import Prefetch
# from django_grapesjs.utils import apply_string_handling
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Post, UserModel, PostCategory
from .serializers import PostListSerializer, PostRetrieveSerializer
from django.core.files.storage import DefaultStorage

from ..attachments.models import Image

# from apps.products.models import ProductCategory
storage = DefaultStorage()


class PostListApiView(generics.ListAPIView):
    queryset = Post.objects.all().order_by('-updated_at')
    serializer_class = PostListSerializer

    def get_queryset(self):
        return Post.objects.prefetch_related(
            Prefetch('author', queryset=UserModel.objects.filter(is_active=True)),
            Prefetch('category', queryset=PostCategory.objects.all()),
        ).filter(is_active=True)


class PostDetailApiView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostRetrieveSerializer
    lookup_field = 'slug'


# class DeleteCommentView(generics.DestroyAPIView):
#     queryset = PostComment.objects.all()
#     serializer_class = PostCommentSerializer
#     permission_classes = [IsAuthenticated, IsPostCommentOwner]
#     lookup_field = 'pk'


# class SiteDocumentDetailApiView(RetrieveAPIView):
#     queryset = SiteDocument.objects.all()

#     def retrieve(self, request, *args, **kwargs):
#         use_html_response = request.GET.get('response', None)
#         instance: SiteDocument = self.get_object()
#         html = instance.html
#         if instance.use_ssr:
#             template = Template(html)
#             context = Context({})
#             rendered_html = template.render(context)
#             html = apply_string_handling(rendered_html)
#         if use_html_response == 'html':
#             return HttpResponse(html)
#         else:
#             return Response({
#                 "html": html,
#             })

IMAGE_UPLOAD_PATH = "uploads/posts/"
IMAGE_UPLOAD_PATH_DATE = "%Y/%m/%d"

class ImageUploadView(APIView):

    def post(self, request):
        post_obj: Post = None
        if 'image' in request.FILES:
            the_file = request.FILES['image']
            allowed_types = [
                'image/jpeg',
                'image/jpg',
                'image/pjpeg',
                'image/x-png',
                'image/png',
                'image/webp',
                'image/gif',
            ]
            if the_file.content_type not in allowed_types:
                return Response(
                    {
                        'success': 0,
                        'message': 'You can only upload images.'
                    },
                )
            filename, extension = os.path.splitext(the_file.name)

            filename += extension

            upload_path = IMAGE_UPLOAD_PATH

            upload_path += datetime.now().strftime(IMAGE_UPLOAD_PATH_DATE)
            path = storage.save(
                os.path.join(upload_path, filename), the_file
            )
            link = storage.url(path)

            new_obj = Image.objects.create(
                name= filename,
                extension = extension,
                url = link,
                size = 0,
                file_type = "attachment",
                parent=post_obj,
            )

            return Response({'success': 1, 'file': {"url": new_obj.url}})
        return Response({'success': 0})
